# gene-extractor
DNA sequence extractor from genes inside CDS in .gbff files

<br>

## English

This script extracts the DNA sequence from genes inside a CDS in .gbff files (NCBI standard).

### How to run the script

The main method to run is direct from powershell, bash or cmd (or other terminal) executing the following command, passing the .gbff file path to be read by parameter:

<code>py gene-extractor.py {YOUR_GBFF_FILE_PATH}</code> or <code>python gene-extractor.py {YOUR_GBFF_FILE_PATH}</code>.

Depending on how is Python installed at the machine this command could be different.

Example: <code>py gene-extractor.py ./temp-files/GCF_000001735.4/genomic.gbff</code>

<br>

Alternatively it's possible to modify the code to run the script. Just change the run statement at the main with some .gbff file path:

<code>run({YOUR_GBFF_FILE_PATH})</code>

Example: <code>run("./temp-files/GCF_000001735.4/genomic.gbff")</code>

<br>

If the .gbff is valid and have valid genes to extract, the genes sequences will be written in a json file named <code>genes-{SOME-RANDOM-UUID}.json</code> in an array.
Now the other sequences will be written in another json file named <code>not-genes-{SOME-RANDOM-UUID}.json</code> in an array for AI purposes.

<br>

## Português

Esse script extrai as sequências de DNA de genes que estão em alguma CDS em arquivos do tipo .gbff (padrão NCBI)

### Como executar o script

A principal forma de executar é a partir do powershell, bash ou cmd (ou outro terminal) executando o comando a seguir, passando o caminho do arquivo .gbff a ser lido por parâmetro:

<code>py gene-extractor.py {CAMINHO_DO_SEU_ARQUIVO_GBFF}</code> ou <code>python gene-extractor.py {CAMINHO_DO_SEU_ARQUIVO_GBFF}</code>. 

Dependendo de como o Python está instalado pode ser um comando diferente.

Exemplo: <code>py gene-extractor.py ./temp-files/GCF_000001735.4/genomic.gbff</code>

<br>

Também é possível modificar o código para rodar o script. É necessário apenas mudar a chamada do método run dentro da main e colocar o caminho de algum arquivo .gbff:

<code>run({CAMINHO_DO_SEU_ARQUIVO_GBFF})</code>

Exemplo: <code>run("./temp-files/GCF_000001735.4/genomic.gbff")</code>

<br>

Se o arquivo .gbff for válido e tiver genes válidos a serem extraídos, as sequencias serão gravadas em um arquivo json chamado <code>genes-{UUID-ALEATÓRIO}.json</code> dentro de um vetor.
Agora as outras sequências também serão gravadas em outro arquivo json chamado <code>not-genes-{UUID-ALEATÓRIO}.json</code> dentro de um vetor para o uso em IA.

<br>
