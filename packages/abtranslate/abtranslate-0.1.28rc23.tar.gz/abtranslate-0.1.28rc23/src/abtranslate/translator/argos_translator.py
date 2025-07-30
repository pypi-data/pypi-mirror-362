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
                logger.info(f"Model initialization error: {e}")
                raise InitializationError(f"Failed to initialize models: {e}")
        
            if self.using_optimized_config:
                if len(sample_data) < BATCH_SIZE: # Only if sample data is sufficient, run the translator tuning.  
                    return base_translator
                try:
                    self.using_optimized_config=False
                    optimized_config = self.get_optimized_config(sample_data)
                    logger.info("Using translator config:", optimized_config)
                    self.apply_translator_config(device=self.device,
                                                 translator_config=optimized_config)
                except Exception as e:
                    logger.info(f"Failed to optimize translator. {e}")
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

        # Store original length to ensure we return the same number of results
        original_length = len(text_list)
        
        # Handle empty/null inputs explicitly
        processed_text_list = []
        empty_indices = []
        
        for i, text in enumerate(text_list):
            if text is None or text == "" or (isinstance(text, str) and text.strip() == ""):
                processed_text_list.append("")
                empty_indices.append(i)
            else:
                processed_text_list.append(text)

        translator = self._initialize_models(processed_text_list[:BATCH_SIZE])
        tokenizer = self.pkg.tokenizer
        sentencizer = self.pkg.sentencizer

        try:
            # Use consistent ignore_empty settings
            expanded_rows = expand_to_sentence_level(processed_text_list, sentencizer, ignore_empty_paragraph=False, ignore_empty_row=False)
            structure = get_structure(expanded_rows, ignore_empty=False)  # ← Changed to False
            sentence_list = flatten_list(expanded_rows, str)
            
            # Handle case where all sentences are empty
            if not sentence_list or all(s == "" for s in sentence_list):
                result = [""] * original_length
                if return_type == pd.Series:
                    return pd.Series(result)
                return result
            
            # Filter out empty sentences for translation but keep track of their positions
            non_empty_sentences = []
            sentence_indices = []
            
            for i, sentence in enumerate(sentence_list):
                if sentence and sentence.strip():
                    non_empty_sentences.append(sentence)
                    sentence_indices.append(i)
            logger.info("Prepared to translate list of sentences: ", non_empty_sentences[:10])
            if non_empty_sentences:
                tokenized_sentences = tokenizer.encode_list(non_empty_sentences)

                if not "max_batch_size" in translation_config.keys():
                    translation_config["max_batch_size"] = BATCH_SIZE

                translation_result = translator.translate_batch(
                    tokenized_sentences,
                    **translation_config
                )
                translated_non_empty = self._parse_translation_result(translation_result)
                
                # Reconstruct the full sentence list with translations
                translated_sentences = [""] * len(sentence_list)
                for i, translated in enumerate(translated_non_empty):
                    translated_sentences[sentence_indices[i]] = translated
            else:
                translated_sentences = [""] * len(sentence_list)

            restored_structure = apply_structure(translated_sentences, structure)
            translated_list = restore_expanded_to_rows_level(restored_structure)
            
            # CRITICAL: Ensure we return exactly the same number of results as input
            if len(translated_list) != original_length:
                logger.warning(f"Length mismatch after translation: expected {original_length}, got {len(translated_list)}")
                # Pad or truncate to match original length
                if len(translated_list) < original_length:
                    translated_list.extend([""] * (original_length - len(translated_list)))
                elif len(translated_list) > original_length:
                    translated_list = translated_list[:original_length]
            
            if return_type == pd.Series:
                return pd.Series(translated_list)
            return translated_list
            
        except Exception as e:
            logger.error(f"Translation batch error: {e}")
            # Return empty strings for all inputs to maintain length
            result = [""] * original_length
            if return_type == pd.Series:
                return pd.Series(result)
            return result

    def get_optimized_config(self, sample_data: List[str]) -> ctranslate2.Translator:
        best_time = float('inf')
        prev_avg = float("inf") 
        patience_count = 0  # Added missing variable initialization

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
        
        logger.info("Starting CPU allocation tuning")
        best_config = None
        for n_inter_threads, n_intra_threads in inter_intra_threads_pairs:
            translator_config["inter_threads"] = n_inter_threads
            translator_config["intra_threads"] = n_intra_threads
            logger.info(f"Testing translation with inter_threads:{n_inter_threads} intra_threads:{n_intra_threads}")
            try:
                self.apply_translator_config(device = self.device, translator_config=translator_config)
            except Exception as e:
                logger.info("Incompatible translator config: ", e)
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
            logger.info(f"Translation finished, average time: {avg_time:.4f}s")

            if avg_time < best_time:
                best_time = avg_time
                best_config = translator_config.copy()
                logger.info("updating best config =>> ", best_config, "\n")
            
            if avg_time > prev_avg:
                patience_count +=1
            else:
                patience_count = 0
            prev_avg = avg_time
        return best_config