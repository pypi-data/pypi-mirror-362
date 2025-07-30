"""
This algorithm was developed and programmed by Ben-Hur Varriano for Sapiens Technology®️
with the goal of providing an “infinite context window” for language models.
The logical foundation of the code is based on extracting features from the prompt and/or a list of dialogues,
retaining only the tokens that best define the message within a predetermined limit. In this way,
the model becomes capable of generalizing the surplus context, assimilating only the general meaning of everything
that was discussed instead of the entire conversation.
This behavior is similar to that of humans, who, although they do not memorize every word in a long conversation,
are able to remember the key points that define what was discussed.

Note: Any public disclosure or comment on the logic and/or operation of this code is strictly prohibited and
the author will be subject to legal proceedings and measures by our team of lawyers.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
class SapiensInfiniteContextWindow:
	def __init__(self):
		from sapiens_embedding import SapiensEmbedding
		from urllib.request import urlopen
		from os.path import isfile
		from re import findall
		from scn import SCN
		from collections import deque
		from copy import deepcopy
		self.__sapiens_embedding = SapiensEmbedding()
		self.__urlopen = urlopen
		self.__isfile = isfile
		self.__findall = findall
		self.__SCN = SCN(show_errors=False)
		self.__deque = deque
		self.__deepcopy = deepcopy
	def __synthesize_tokens(self, text='', maximum_tokens=0, pattern='', separator=''):
		result_text = ''
		text = result_text = rf'{text}'.strip()
		maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
		pattern = str(pattern).lower().strip()
		if not text or maximum_tokens < 1: return ''
		separation_tokens = []
		if separator: separation_tokens = self.__sapiens_embedding.text_to_embedding(text_data='...', pattern=pattern)
		if separation_tokens: maximum_tokens = max(0, maximum_tokens-len(separation_tokens))
		if maximum_tokens > 0:
			embedding = self.__sapiens_embedding.text_to_embedding(text_data=text, pattern=pattern)
			embedding_length = len(embedding)
			if maximum_tokens >= embedding_length: return result_text
			parts_length = maximum_tokens//3
			embedding_start = embedding[:parts_length]
			middle_position = (embedding_length//2)-1
			embedding_middle = embedding[middle_position:middle_position+parts_length]
			embedding_end = embedding[-parts_length:]
			if separation_tokens: final_embedding = embedding_start+separation_tokens+embedding_middle+separation_tokens+embedding_end
			else: final_embedding = embedding_start+embedding_middle+embedding_end
			result_text = self.__sapiens_embedding.embedding_to_text(embedding=final_embedding, length=maximum_tokens, pattern=pattern)
		else: result_text = ''
		return result_text
	def __guarantee(self, result_text='', text='', maximum_tokens=0, pattern=''):
		try:
			result_text, text = rf'{result_text}'.strip(), rf'{text}'.strip()
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			pattern = str(pattern).lower().strip()
			if maximum_tokens < 1: return ''
			tokens_counted = self.__sapiens_embedding.count_tokens(text_data_or_embedding=result_text, pattern=pattern)
			bigger = tokens_counted > maximum_tokens
			if bigger or len(result_text) < 1:
				embedding = self.__sapiens_embedding.text_to_embedding(text_data=result_text if bigger else text, pattern=pattern)
				embedding = embedding[-maximum_tokens:]
				result_text = self.__sapiens_embedding.embedding_to_text(embedding=embedding, length=maximum_tokens, pattern=pattern)
			result_text = rf'{result_text}'.strip()
			if len(result_text) < 1: result_text = '?'
			return result_text
		except:
			result_text, text = str(result_text).strip(), str(text).strip()
			result_text_length, text_length = len(result_text), len(text)
			if result_text_length < 1: result_text = '?'
			if text_length < 1: text = '?'
			return text[-maximum_tokens:] if text_length > result_text_length else result_text[-maximum_tokens:]
	def __read_txt(self, file_path='', strip=True):
		txt_content = ''
		file_path = str(file_path).strip()
		if file_path.startswith(('http://', 'https://', 'www.')):
			try:
				connection = self.__urlopen(file_path)
				txt_content = rf"{connection.read().decode('utf-8')}"
			except: txt_content = ''
		if not txt_content and file_path and self.__isfile(file_path):
			with open(file_path, 'r', encoding='utf-8') as text_file: txt_content = rf'{text_file.read()}'
		return txt_content if not strip else txt_content.strip()
	def __extract_segments_from_string(self, text=''):
	    block_list = []
	    marker_count = text.count('```')
	    if marker_count == 0 or marker_count % 2 != 0: return []
	    position = 0
	    while True:
	        start = text.find('```', position)
	        if start == -1:
	            block = text[position:].strip()
	            if block: block_list.append(block)
	            break
	        if start > position:
	          block = text[position:start].strip()
	          block_list.append(block)
	        end = text.find('```', start+3)
	        if end == -1: break
	        block = text[start:end+3].strip()
	        if block: block_list.append(block)
	        position = end+3
	    return block_list
	def load_vocabulary(self, file_path=''):
		try: return self.__sapiens_embedding.load_vocabulary(file_path=file_path)
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.load_vocabulary: ' + str(error))
			return False
	def synthesize_code(self, text='', maximum_tokens=0, pattern=''):
		try:
			result_text = ''
			text = result_text = rf'{text}'.strip()
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			pattern = str(pattern).lower().strip()
			if not text or maximum_tokens < 1: return ''
			code_lines = text.split('\n')
			def _apply_synthesis(declaration_markers=[]):
				new_code_lines = []
				for code_line in code_lines:
					original_code_line = code_line
					code_line = str(code_line).strip()
					for declaration_marker in declaration_markers:
						if code_line.startswith(declaration_marker) or code_line.endswith(declaration_marker):
							indentations_count, character = len(original_code_line) - len(original_code_line.lstrip('\t')), '\t'
							if indentations_count < 1: indentations_count, character = len(original_code_line) - len(original_code_line.lstrip(' ')), ' '
							increment = f'\n{character*indentations_count}...' if '```' not in code_line else ''
							new_code_lines.append(original_code_line+increment)
				return '\n'.join(new_code_lines).strip()
			tokens_counted, declaration_markers, iterations = float('inf'), ('```', ':', ')', '{', '#', '"""', "'''", '//', '/*', '*/', '<!--', '-->'), 0
			declaration_markers_length = len(declaration_markers)
			while tokens_counted > maximum_tokens:
				result_text = _apply_synthesis(declaration_markers=declaration_markers[:-iterations] if iterations > 0 else declaration_markers)
				tokens_counted = self.__sapiens_embedding.count_tokens(text_data_or_embedding=rf'{result_text}', pattern=pattern)
				iterations += 1
				if iterations >= declaration_markers_length: break
			tokens_counted = self.__sapiens_embedding.count_tokens(text_data_or_embedding=rf'{result_text}', pattern=pattern)
			if tokens_counted > maximum_tokens: result_text = self.__synthesize_tokens(text=result_text, maximum_tokens=maximum_tokens, pattern=pattern, separator='... ')
			result_text = self.__guarantee(result_text=result_text, text=text, maximum_tokens=maximum_tokens, pattern=pattern)
			return result_text
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.synthesize_code: ' + str(error))
			return self.__guarantee(result_text='', text=text, maximum_tokens=maximum_tokens, pattern=pattern)
	def synthesize_code_file(self, file_path='', maximum_tokens=0, pattern=''):
		try:
			result_text = ''
			file_path = str(file_path).strip()
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			pattern = str(pattern).lower().strip()
			if not file_path or maximum_tokens < 1: return result_text
			if not file_path.startswith(('http://', 'https://', 'www.')) and not self.__isfile(file_path):
				print(f'The file at path {file_path} was not found.')
				return result_text
			text = self.__read_txt(file_path=file_path)
			result_text = self.synthesize_code(text=text, maximum_tokens=maximum_tokens, pattern=pattern)
			return result_text
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.synthesize_code_file: ' + str(error))
			return '?'
	def synthesize_tokens(self, prompt='', text='', maximum_tokens=0, pattern=''):
		try:
			result_text = ''
			prompt, text = str(prompt).strip(), str(text).strip()
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			if maximum_tokens < 1: return result_text
			def _get_new_sentences(string_segment=''):
				def __split_by_punctuation(string=''): return self.__findall(r'[^.;?!]+[.;?!]', str(string).strip())
				sentences_list, new_sentences = __split_by_punctuation(string=string_segment), []
				for sentence in sentences_list:
					sentence = sentence.strip()
					probability = self.__SCN.textualComparison(text1=prompt, text2=sentence, consider_length=False)
					if probability >= .5: new_sentences.append(sentence)
				return new_sentences
			string_segments = self.__extract_segments_from_string(text=text)
			if string_segments:
				segments_number = len(string_segments)
				maximum_tokens_per_segment = (maximum_tokens//segments_number)-(segments_number-1)
				if maximum_tokens_per_segment > 0:
					for index, string_segment in enumerate(string_segments):
						marker_count = string_segment.count('```')
						if marker_count > 0 and marker_count % 2 == 0: string_segments[index] = self.synthesize_code(text=string_segment, maximum_tokens=maximum_tokens_per_segment, pattern=pattern)
						else:
							if prompt:
								new_sentences = _get_new_sentences(string_segment=string_segment)
								if new_sentences: string_segment = '\n'.join(new_sentences).strip()
							string_segments[index] = self.__synthesize_tokens(text=string_segment, maximum_tokens=maximum_tokens_per_segment, pattern=pattern, separator='... ')
					result_text = '\n'.join(string_segments)
			if not result_text:
				if prompt:
					new_sentences = _get_new_sentences(string_segment=text)
					if new_sentences: text = '\n'.join(new_sentences).strip()
				result_text = self.__synthesize_tokens(text=text, maximum_tokens=maximum_tokens, pattern=pattern, separator='... ')
			result_text = self.__guarantee(result_text=result_text, text=text, maximum_tokens=maximum_tokens, pattern=pattern)
			return result_text
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.synthesize_tokens: ' + str(error))
			return self.__guarantee(result_text='', text=text, maximum_tokens=maximum_tokens, pattern=pattern)
	def synthesize_tokens_txt(self, prompt='', file_path='', maximum_tokens=0, pattern=''):
		try:
			result_text = ''
			file_path = str(file_path).strip()
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			pattern = str(pattern).lower().strip()
			if not file_path or maximum_tokens < 1: return result_text
			if not file_path.startswith(('http://', 'https://', 'www.')) and not self.__isfile(file_path):
				print(f'The file at path {file_path} was not found.')
				return result_text
			text = self.__read_txt(file_path=file_path)
			result_text = self.synthesize_tokens(text=text, prompt=prompt, maximum_tokens=maximum_tokens, pattern=pattern)
			return result_text
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.synthesize_tokens_txt: ' + str(error))
			return '?'
	def synthesize_messages(self, prompt='', messages=[], maximum_tokens=0, pattern='', keys=('content',)):
		try:
			result_dictionary = {'messages': messages, 'synthesis': messages}
			messages = list(messages) if type(messages) in (tuple, list) else []
			maximum_tokens = max(0, int(maximum_tokens)) if type(maximum_tokens) in (bool, int, float) else 0
			pattern = str(pattern).lower().strip()
			keys = tuple(keys) if type(messages) in (tuple, list) else []
			if not messages or maximum_tokens < 1: return result_dictionary
			def _has_value_in_dictionary(dictionary={}, target_value=''):
				if isinstance(dictionary, dict):
					for current_value in dictionary.values():
						if current_value == target_value: return True
						if isinstance(current_value, dict):
							if _has_value_in_dictionary(current_value, target_value): return True
						if isinstance(current_value, list):
							for element in current_value:
								if isinstance(element, dict):
									if _has_value_in_dictionary(element, target_value): return True
								if element == target_value: return True
			def _find_key_element(messages=[], key_name='', ignore_indexes=[], ignore_messages=[], max_tokens=0):
				for index, dictionary in enumerate(messages):
					if index in ignore_indexes: continue
					queue = self.__deque([(dictionary, [])])
					while queue:
						current, path = queue.popleft()
						if isinstance(current, dict):
							for key, value in current.items():
								new_path = path + [key]
								if key == key_name and isinstance(value, str):
									element = self.__deepcopy(messages[index])
									if element not in ignore_messages:
										target = element
										for element_path in new_path[:-1]: target = target[element_path]
										if max_tokens > 0: target[key_name] = self.synthesize_tokens(prompt=prompt, text=value, maximum_tokens=max_tokens, pattern=pattern)
										if target[key_name] and target[key_name].strip() not in ('...', '?'): return element, index
								if isinstance(value, dict) or isinstance(value, list): queue.append((value, new_path))
						elif isinstance(current, list):
							for new_index, item in enumerate(current): queue.append((item, path+[new_index]))
				return {}, -1
			messages_length = len(messages)
			fifty_percent = max(0, maximum_tokens//2)
			if fifty_percent < 1: return result_dictionary
			if messages_length > 5:
				if _has_value_in_dictionary(dictionary=messages[0], target_value='system'): first_dialogue = [messages[0], messages[1], messages[2]]
				else: first_dialogue = [messages[0], messages[1]]
				last_dialogue = [messages[-2], messages[-1]]
				main_dialogues = first_dialogue+last_dialogue
			else: main_dialogues = []
			main_dialogues_length = len(main_dialogues)
			maximum_remaining_tokens = fifty_percent//max(1, messages_length-main_dialogues_length) if main_dialogues else maximum_tokens//max(1, messages_length)
			if main_dialogues and maximum_remaining_tokens <= 500:
				if main_dialogues_length == 5: main_dialogues = [main_dialogues[0], main_dialogues[1], main_dialogues[2], main_dialogues[-1]]
				elif main_dialogues_length == 4: main_dialogues = [main_dialogues[0], main_dialogues[1], main_dialogues[-1]]
				messages = main_dialogues
				main_dialogues = []
				maximum_remaining_tokens = maximum_tokens//max(1, main_dialogues_length)
			elif maximum_remaining_tokens <= 1000: main_dialogues, maximum_remaining_tokens = [], maximum_tokens//max(1, messages_length)
			if main_dialogues:
				ignore_indexes, ignore_messages, new_messages = [], main_dialogues, []
				maximum_main_tokens = fifty_percent//max(1, len(ignore_messages))
				for ignore_message in ignore_messages: messages.remove(ignore_message)
				for key_name in keys:
					key_element = True
					while key_element:
						key_element, index = _find_key_element(messages=main_dialogues, key_name=key_name, ignore_indexes=ignore_indexes, ignore_messages=[], max_tokens=maximum_main_tokens)
						if key_element and index >= 0: new_messages.append(key_element), ignore_indexes.append(index)
						else: break
				main_dialogues = new_messages
			main_dialogues_length = len(main_dialogues)
			ignore_indexes, ignore_messages, new_messages = [], main_dialogues, []
			for key_name in keys:
				key_element = True
				while key_element:
					key_element, index = _find_key_element(messages=messages, key_name=key_name, ignore_indexes=ignore_indexes, ignore_messages=ignore_messages, max_tokens=maximum_remaining_tokens)
					if key_element and index >= 0: new_messages.append(key_element), ignore_indexes.append(index)
					else: break
			if main_dialogues_length == 5: new_messages = [main_dialogues[0], main_dialogues[1], main_dialogues[2]]+new_messages+[main_dialogues[-2], main_dialogues[-1]]
			elif main_dialogues_length == 4: new_messages = [main_dialogues[0], main_dialogues[1]]+new_messages+[main_dialogues[-2], main_dialogues[-1]]
			if new_messages: result_dictionary['synthesis'] = new_messages
			return result_dictionary
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.synthesize_messages: ' + str(error))
			return {'messages': messages, 'synthesis': messages}
	def count_tokens(self, text='', pattern=''):
		try: return self.__sapiens_embedding.count_tokens(text_data_or_embedding=rf'{text}', pattern=pattern)
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.count_tokens: ' + str(error))
			return 0
	def count_tokens_txt(self, file_path='', pattern=''):
		try:
			tokens_counted = 0
			file_path = str(file_path).strip()
			pattern = str(pattern).lower().strip()
			if not file_path: return tokens_counted
			if not file_path.startswith(('http://', 'https://', 'www.')) and not self.__isfile(file_path):
				print(f'The file at path {file_path} was not found.')
				return tokens_counted
			text = self.__read_txt(file_path=file_path, strip=False)
			tokens_counted = self.count_tokens(text=text, pattern=pattern)
			return tokens_counted
		except Exception as error:
			print('ERROR in SapiensInfiniteContextWindow.count_tokens_txt: ' + str(error))
			return 0
"""
This algorithm was developed and programmed by Ben-Hur Varriano for Sapiens Technology®️
with the goal of providing an “infinite context window” for language models.
The logical foundation of the code is based on extracting features from the prompt and/or a list of dialogues,
retaining only the tokens that best define the message within a predetermined limit. In this way,
the model becomes capable of generalizing the surplus context, assimilating only the general meaning of everything
that was discussed instead of the entire conversation.
This behavior is similar to that of humans, who, although they do not memorize every word in a long conversation,
are able to remember the key points that define what was discussed.

Note: Any public disclosure or comment on the logic and/or operation of this code is strictly prohibited and
the author will be subject to legal proceedings and measures by our team of lawyers.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
