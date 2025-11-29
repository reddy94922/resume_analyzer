candidates = {
    'PromptTemplate': [
        'langchain.prompts.prompt',
        'langchain.prompts',
        'langchain_core.prompts',
        'langchain_core.prompts.prompt'
    ],
    'LLMChain': [
        'langchain.chains',
        'langchain.chains.llm',
        'langchain_core.chains',
        'langchain_core.chains.llm'
    ],
    'OpenAIEmbeddings': [
        'langchain.embeddings',
        'langchain_openai',
        'langchain_openai.embeddings'
    ],
    'FAISS': [
        'langchain.vectorstores',
        'langchain_community.vectorstores',
        'langchain_community.vectorstores.faiss'
    ],
    'Document': [
        'langchain.schema',
        'langchain_core.documents',
        'langchain.docstore.document'
    ]
}

import importlib

for name, modules in candidates.items():
    found = False
    for mod in modules:
        try:
            m = importlib.import_module(mod)
            attrs = [a for a in dir(m) if not a.startswith('_')]
            print(f"OK: {name} might be in {mod}; sample attrs: {attrs[:10]}")
            found = True
        except Exception as e:
            print(f"ERR: cannot import {mod}: {e}")
    if not found:
        print(f"NOT FOUND: {name} in any tried modules\n")
