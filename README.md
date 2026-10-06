# desconfIA

Is a system that analyzes data and presents results to assist users in evaluating the reliability of information about financial scams.
 - The goal is to analyze data and provide results to support the verification of financial scams conveyed in diverse media, preserving human critical thinking.

O aplicativo desconfIAnanalisa o texto de uma mensagem e estima a probabilidade de ela ser smishing (golpe por SMS). O resultado é uma indicação automatizada e não substitui a avaliação do usuário.

## Requisitos


- Python 3.13 64 bits. Esta é a versão usada para validar a execução do projeto.
- Git, se for clonar o repositório.
- A pasta do modelo treinado `modelo_extraid`, descrita abaixo.
- Acesso à internet para instalar as dependências com `pip`.

As versões das bibliotecas estão fixadas em [`requirements.txt`](./requirements.txt). O tokenizer usa a implementação Python WordPiece do KerasHub; não instale `tensorflow-text` para executar o app no Windows.

## Obter o projeto

Clone o repositório e entre na pasta:

```powershell
git clone https://github.com/carlosmandele/desconfIA-project.git
cd desconfIA-project
```

Se o projeto já estiver na sua máquina, abra o PowerShell na pasta raiz do repositório, onde estão `app.py` e `requirements.txt`.

## Preparar o modelo

O aplicativo carrega o modelo do caminho relativo `modelo_extraid`. Essa pasta precisa estar na raiz do projeto e conter, no mínimo:

```text
modelo_extraid/
├── config.json
├── metadata.json
├── model.weights.h5
└── assets/
    └── preprocessor/
        └── tokenizer/
            └── vocabulary.txt
```

O modelo treinado não está versionado no repositório. Obtenha a pasta `modelo_extraid` da equipe responsável pelo projeto e coloque-a na raiz, sem renomear os arquivos. O arquivo de pesos tem aproximadamente 603 MB.

## Instalar dependências no Windows

Na raiz do projeto, crie e ative um ambiente virtual:

```powershell
py -3.13 -m venv env
.\env\Scripts\Activate.ps1
```

Instale as dependências fixadas:

```powershell
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação do ambiente, use o Prompt de Comando (CMD):

```bat
env\Scripts\activate.bat
python -m pip install -r requirements.txt
```

## Executar o aplicativo

Com o ambiente virtual ativado e a pasta do modelo no lugar, execute a partir da raiz:

```powershell
streamlit run app.py
```

O Streamlit exibirá um endereço local no terminal (normalmente `http://localhost:8501`) e poderá abrir a página no navegador.

1. Digite ou cole uma mensagem SMS no campo **Texto da Mensagem**.
2. Clique em **Analisar Mensagem**.
3. Consulte o diagnóstico e as probabilidades de smishing e de mensagem legítima.

Mensagens vazias são recusadas pela interface. O limiar de classificação atualmente usado é `0.5343`. Uma probabilidade é uma estimativa do modelo, não uma garantia de que a mensagem seja segura ou fraudulenta.

## Testar a execução

O repositório não contém uma suíte de testes automatizados. Faça um teste manual após iniciar o app:

1. Confirme que a página abriu e que a mensagem de boas-vindas aparece.
2. Clique em **Analisar Mensagem** com o campo vazio e confirme que a orientação para digitar uma mensagem é exibida.
3. Analise uma mensagem de teste não sensível e confirme que o diagnóstico e as duas métricas de probabilidade aparecem.
4. Analise um texto longo e confirme que a aplicação conclui a análise sem erro.
5. Interrompa o servidor com `Ctrl+C` no terminal.

As métricas podem variar se os pesos do modelo forem diferentes. Não use o resultado como única base para decidir se um SMS, link ou pedido de pagamento é legítimo.

## Notebooks

Os diretórios notebooks contêm material de treinamento e exploração de dados. Eles não são necessários para iniciar o aplicativo Streamlit. Para executá-los, será necessário configurar Jupyter no ambiente e disponibilizar os dados que cada notebook referencia.

## Solução de problemas

- **A pasta ou os arquivos do modelo não foram encontrados:** confira se `modelo_extraid` está na raiz do projeto e contém os arquivos listados em [Preparar o modelo](#preparar-o-modelo).
- **Erro ao instalar as dependências:** confirme que o Python selecionado é 3.13 de 64 bits, que o ambiente virtual está ativado e que há acesso à internet; depois repita `python -m pip install -r requirements.txt`.
- **Erro envolvendo `tensorflow_text` ou `FastWordpieceTokenizer`:** confirme que está executando a versão atual de `app.py`, que usa o tokenizer Python incluído no KerasHub. O app não requer `tensorflow-text`.
- **Aviso de `tf.reset_default_graph` obsoleto no terminal:** é um aviso de compatibilidade emitido internamente pelo Keras/TensorFlow; isoladamente, não indica falha na análise.
- **Aviso sobre GPU no Windows:** o TensorFlow utilizado executa a inferência na CPU no Windows nativo. Esse aviso, por si só, não impede a execução.