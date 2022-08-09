# github-quality-assurance
Desafio de QA da uTech para validar algumas funções do Github.

Foi feito usando Python e Selenium e valida as seguintes funções:

- Login
- Pesquisa
- Criação de repositórios
- Deleção de repositórios

## Login
Para validar o login, o teste feito é procurar uma mensagem de erro na paǵina. Caso uma mensagem de erro não seja encontrada após submeter o login, ele é validado.

## Pesquisa
Para validar a pesquisa, foi usada uma lista com várias palavras comuns. A partir delas foram feitas duas etapas de verificação: a primeira consiste em verificar se em cada teste de pesquisa, ao menos metade das categorias de resultados tiveram mais que 0 resultados. Por exemplo, se foram consideradas as categorias commits, users, discussions e issues e apenas discussions teve 0 ocorrências, essa etapa é validada.

A segunda etapa consiste em procurar o termo de pesquisa em todos os títulos e descrições de resultados. Por exemplo, se tiveram 6 resultados carregados, terão 6 títulos e 6 descrições, no total 12. Caso o termo de pesquisa esteja contido em pelo menos metade desses elementos, ou seja, 6, essa etapa é validada.

A pesquisa de uma palavra é validada caso ambas as etapas passem sem erros.

## Criação de repositórios
Para validar a criação de repositórios, é gerado um nome de repositório aleatório e, em seguida, é marcada a opção de repositório privado. Após isso o botão de criar repositório é ativado e, caso o sistema detecte uma nova página que possua o botão para a aba de "código", que é presente apenas em páginas de repositórios, a criação de repositórios é validada pois significa que o repositório foi criado e o navegador já foi redirecionado para sua página.

## Deleção de repositórios
Para validar a deleção de repositórios, o código é executado logo em seguida da criação de um novo repositório. É aberta a aba de configurações do repositório, em seguida o nome do repositório é salvo a partir da caixa de input para mudar o nome do repositório. Em seguida o botão para deletar o repositório é ativado e, no input de confirmação de deleção, é usado o nome de usuário definido no início da execução do código e o nome do repositório. Após isso o botão de confirmar deleção é ativo.

Para verificar se a deleção ocorreu com sucesso, é verificado se a página atual é a de todos os repositórios do usuário. O que por si só já significa sucesso. Mas, como uma segunda etapa, o endereço para o repositório deletado é acessado e, caso as imagens de erro 404 sejam retornadas, a deleção de repositórios é validada.

## Persistência de dados
O projeto também possuí persistência de dados. Caso deseje, o usuário pode salvar suas credenciais de login localmente para poupar tempo durante os testes.

# Como executar o código?

- Instalar o package Selenium para Python. (Pode ser feito pelo comando `pip install selenium`)

- Baixar a última versão do geckodriver em https://github.com/mozilla/geckodriver/releases

- No diretório do arquivo baixado, executar os seguintes comandos:

### Extrair arquivo
- `tar -xvzf geckodriver*`

### Torná-lo executável
- `chmod +x geckodriver`

### Adicionar o geckodriver ao PATH
- `sudo mv geckodriver /usr/local/bin/`

### Caso um erro para executar o Firefox seja apresentado:
#### (Isso irá desinstalar o Firefox pelo snap e irá instalá-lo pelo apt)

`sudo snap remove firefox`

`sudo add-apt-repository ppa:mozillateam/ppa`
```
echo '
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001
' | sudo tee /etc/apt/preferences.d/mozilla-firefox
```
`sudo apt install firefox`
