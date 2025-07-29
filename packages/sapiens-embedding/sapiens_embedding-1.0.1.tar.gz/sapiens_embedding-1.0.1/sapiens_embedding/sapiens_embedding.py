# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
# algorithm specialized in incorporating tokens with the gpt and sapi standard
class SapiensEmbedding:
	def __init__(self):
		from sapiens_tokenizer import SapiensTokenizer
		self.__sapiens_tokenizer = SapiensTokenizer()
	def load_vocabulary(self, file_path=''):
		try: return self.__sapiens_tokenizer.load_vocabulary(file_path=file_path)
		except Exception as error:
			print('ERROR in SapiensEmbedding.load_vocabulary: ' + str(error))
			return False
	def text_to_embedding(self, text_data='', length=None, pattern='', method='truncate'):
		try:
			embedding = []
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not text_data or length == 0: return embedding
			pattern, method = str(pattern).lower().strip(), str(method).lower().strip()
			text_data = rf'{text_data}'.strip()
			if method not in ('truncate', 'average'): method = 'truncate'
			if method == 'truncate' or length is None: embedding = self.__sapiens_tokenizer.to_encode(text_data=text_data, length=length, pattern=pattern)
			else:
				embedding = self.__sapiens_tokenizer.to_encode(text_data=text_data, length=None, pattern=pattern)
				embedding_length = len(embedding)
				if embedding_length < length:
					complement_id = self.__sapiens_tokenizer.to_encode(text_data='_', length=None, pattern=pattern)
					embedding += [complement_id]*(length-embedding_length)
				else:
					embedding_limit = max(0, length-1)
					initial_embedding = embedding[:embedding_limit]
					remaining_embedding = embedding[embedding_limit:]
					last_token_id = int(sum(remaining_embedding)/max(1, len(remaining_embedding)))
					embedding = initial_embedding+[last_token_id]
			return embedding
		except Exception as error:
			print('ERROR in SapiensEmbedding.text_to_embedding: ' + str(error))
			return []
	def embedding_to_text(self, embedding=[], length=None, pattern='', strip=True):
		try:
			text_data = ''
			embedding = list(embedding) if type(embedding) in (tuple, list) else []
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not embedding or length == 0: return text_data
			pattern = str(pattern).lower().strip()
			strip = bool(strip) if type(strip) in (bool, int, float) else True
			text_data = self.__sapiens_tokenizer.to_decode(embedding=embedding, length=length, pattern=pattern)
			if '_' in text_data: text_data = text_data.rstrip('_')+' '*(len(text_data)-len(text_data.rstrip('_')))
			return text_data if not strip else text_data.strip()
		except Exception as error:
			print('ERROR in SapiensEmbedding.embedding_to_text: ' + str(error))
			return ''
	def count_tokens(self, text_data_or_embedding='', pattern=''):
		try: return self.__sapiens_tokenizer.count_tokens(text_data_or_embedding=text_data_or_embedding, pattern=pattern)
		except Exception as error:
			print('ERROR in SapiensEmbedding.count_tokens: ' + str(error))
			return 0
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
