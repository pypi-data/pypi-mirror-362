from __future__ import annotations
from typing import List, Union, Dict, TYPE_CHECKING
import os
import psutil
import time

import pyspark
import sentencepiece as spm
import ctranslate2
import stanza
import pandas as pd

from abtranslate.config import CT2TranslatorConfig, CT2TranslationConfig
from abtranslate.config.constants import DEFAULT_CT2_CONFIG, DEFAULT_CT2_TRANSLATION_CONFIG, BATCH_SIZE
from abtranslate.utils.logger import logger
from abtranslate.utils.helper import generate_batch, expand_to_sentence_level, get_structure, apply_structure, restore_expanded_to_rows_level,  flatten_list
from abtranslate.utils.exception import InitializationError

if TYPE_CHECKING:
    from translator.package import ArgosPackage

class ArgosTranslator:
    def __init__(self, package: ArgosPackage, device:str ="cpu", translator_config: CT2TranslatorConfig = DEFAULT_CT2_CONFIG, optimized_config=False):
        if device == "gpu":
            translator_config == {}
            optimized_config = False
        self.translator_config = translator_config
        self.device = device
        self.pkg = package
        self.translator = None
        self.using_optimized_config = optimized_config

    def _initialize_models(
        self,
        sample_data
    ) -> ctranslate2.Translator:
        """
        Initialize all required models for translation.
        
        Args:
            compute_type: Computation type for CTranslate2
            inter_threads: Number of inter-threads
            intra_threads: Number of intra-threads
            
        Raises:
            ModelInitializationError: If any model fails to initialize
        """
        if (not self.translator) or self.using_optimized_config:
            try:
                base_translator = ctranslate2.Translator(
                        self.pkg.get_model_path(),
                        self.device,
                        **self.translator_config
                    ) 
            except Exception as e:
                print(f"Model initialization error: {e}")
                raise InitializationError(f"Failed to initialize models: {e}")
        
            if self.using_optimized_config:
                if len(sample_data) < BATCH_SIZE: # Only if sample data is sufficient, run the translator tuning.  
                    return base_translator
                try:
                    self.using_optimized_config=False
                    optimized_config = self.get_optimized_config(sample_data)
                    print("Using translator config:", optimized_config)
                    self.apply_translator_config(device=self.device,
                                                 translator_config=optimized_config)
                except Exception as e:
                    print(f"Failed to optimize translator. {e}")
                    self.translator = base_translator
                    self.using_optimized_config=False
            else:   
                self.translator = base_translator

        return self.translator

    def apply_translator_config(self, device, translator_config):
        self.translator = ctranslate2.Translator(
                        self.pkg.get_model_path(),
                        device,
                        **translator_config
                    ) 
        
    def _text_preprocessing(self, text: str) -> List[str]:
        tokenizer = self.pkg.tokenizer
        sentences = self.pkg.sentencizer.split_sentences(text) # stanza
        encoded_tokens = [tokenizer.encode(sentence) for sentence in sentences]  # SentencePiece
        return encoded_tokens
    
    def _parse_translation_result(self, ct2_outputs: ctranslate2.TranslationResult) -> List[str]:
        tokenizer = self.pkg.tokenizer
        translated_tokens = [output.hypotheses[0] for output in ct2_outputs]
        translations_detok = [tokenizer.decode(tokens) for tokens in translated_tokens]
        return translations_detok

    def translate(self, input_text:str, translation_config: CT2TranslationConfig = DEFAULT_CT2_TRANSLATION_CONFIG) -> str: 
        """
        Translate a sentence using CTranslate2 and shared SentencePiece model.

        Args:
            input (str): Source sentence to translate
            translator (ctranslate2.Translator): Loaded CTranslate2 model
            sp_model (sentencepiece.SentencePieceProcessor): Loaded shared SentencePiece model

        Returns:
            str: Translated sentence
        """
        translation_result = self.translate_batch([input_text], translation_config) 
        return  translation_result[0]

    def translate_batch(self, text_list: List[str] | pd.Series, translation_config: CT2TranslationConfig = DEFAULT_CT2_TRANSLATION_CONFIG, return_type = List) -> List[str]:
        if isinstance(text_list, pd.Series):
            text_list = text_list.tolist()
            return_type = pd.Series

        translator = self._initialize_models(text_list[:BATCH_SIZE])
        tokenizer = self.pkg.tokenizer
        sentencizer =self.pkg.sentencizer

        expanded_rows = expand_to_sentence_level(text_list, sentencizer, ignore_empty_paragraph=True, ignore_empty_row=False)
        structure = get_structure(expanded_rows, ignore_empty=True)
        sentence_list = flatten_list(expanded_rows, str)
        tokenized_sentences = tokenizer.encode_list(sentence_list)

        if not "max_batch_size" in translation_config.keys():
            translation_config["max_batch_size"] = BATCH_SIZE

        translation_result = translator.translate_batch(
            tokenized_sentences,
            **translation_config
        )
        translated_sentences = self._parse_translation_result(translation_result)
        restored_structure = apply_structure(translated_sentences, structure)
        translated_list = restore_expanded_to_rows_level(restored_structure)
        
        if return_type == pd.Series:
            return pd.Series(translated_list)
        return translated_list

    def get_optimized_config(self, sample_data: List[str]) -> ctranslate2.Translator:
        best_time = float('inf')
        prev_avg = float("inf") 

        translator_config = self.translator_config.copy()
        translator_config["compute_type"] = "int8_float32"
        translation_config = {  "beam_size": 1,
                                "num_hypotheses": 1, 
                                "replace_unknowns": False,}
        
        logical_cpu_count = psutil.cpu_count(logical=False)
        inter_intra_threads_pairs = [(1,                        0), 
                                    (1,                        logical_cpu_count),
                                    (logical_cpu_count//2,      2),
                                    ((logical_cpu_count//2)-1,  2),    
                                    (logical_cpu_count,        0),  
                                    (2,                        logical_cpu_count//2),
                                    (2,                        (logical_cpu_count//2)-1),
                                    (1,                        logical_cpu_count)]
        
        print("Starting CPU allocation tuning")
        best_config = None
        for n_inter_threads, n_intra_threads in inter_intra_threads_pairs:
            translator_config["inter_threads"] = n_inter_threads
            translator_config["intra_threads"] = n_intra_threads
            print(f"Testing translation with inter_threads:{n_inter_threads} intra_threads:{n_intra_threads}")
            try:
                self.apply_translator_config(device = self.device, translator_config=translator_config)
            except Exception as e:
                print("Incompatible translator config: ", e)
                continue
            runtimes = []
            try:
                for _ in range(4):
                    start = time.perf_counter()
                    self.translate_batch(sample_data, translation_config)
                    end = time.perf_counter()
                    runtimes.append(end - start)
            except:
                raise Exception(f"Error during testing translator config{translator_config}")
            avg_time = sum(runtimes) / len(runtimes)
            print(f"Translation finished, average time: {avg_time:.4f}s")

            if avg_time < best_time:
                best_time = avg_time
                best_config = translator_config.copy()
                print("updateing best config =>> ", best_config, "\n")
            
            if avg_time > prev_avg:
                patience_count +=1
            else:
                patience_count = 0
            prev_avg = avg_time
        print("FINISDHED, best is: ", best_config)
        return best_config