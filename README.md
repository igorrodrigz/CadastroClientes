# Sistema de Controle de Clientes 

## Descrição

O **Sistema de Controle de Clientes - LL Cutelaria** é uma aplicação desenvolvida para gerenciar clientes e suas respectivas compras para a empresa MEI LL Cutelaria. A aplicação permite a inclusão, edição e exclusão de clientes e compras, além da visualização detalhada das informações dos clientes e suas compras.

## Funcionalidades

- **Gerenciamento de Clientes**
  - Adicionar novos clientes
  - Editar dados de clientes existentes
  - Excluir clientes
  - Buscar clientes por nome ou CPF

- **Gerenciamento de Compras**
  - Adicionar novas compras para um cliente
  - Editar informações de compras existentes
  - Excluir compras
  - Visualizar todas as compras associadas a um cliente

## Tecnologias Utilizadas

- **PyQt5**: Framework para desenvolvimento da interface gráfica.
- **SQLite**: Banco de dados relacional para armazenar informações de clientes e compras.

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicializa o aplicativo e configura a janela principal.
- `client_window.py`: Módulo responsável pela janela de detalhes do cliente e suas compras.
- `lojaDB.py`: Módulo que contém funções para interação com o banco de dados SQLite.
- `utils.py`: Módulo com funções utilitárias, como criação de seletores de data.
- `logos/`: Pasta contendo ícones e logotipos utilizados na aplicação.

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/igorrodrigz/sistema-controle-clientes.git
   ```

2. **Instale as dependências:**

   Certifique-se de ter o Python e o PyQt5 instalados. Você pode instalar o PyQt5 usando o seguinte comando:

   ```bash
   pip install pyqt5
   ```

3. **Inicialize o banco de dados:**

   Execute o arquivo `main.py` para criar o banco de dados e as tabelas necessárias.

   ```bash
   python main.py
   ```

## Uso

1. **Inicie a aplicação:**

   Execute o arquivo `main.py` para iniciar a aplicação.

   ```bash
   python main.py
   ```

2. **Interface Principal:**

   - Utilize a barra de busca para procurar clientes por nome ou CPF.
   - Utilize os botões para adicionar, editar, excluir clientes e acessar detalhes de um cliente.
   - Na tela de detalhes do cliente, você pode gerenciar as compras associadas a ele.

## Contribuições

Contribuições são bem-vindas! Para contribuir com o projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para a sua feature ou correção.
3. Faça suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou mais informações, entre em contato com:

- **Email:** rodrigues.igor.ir@gmail.com
```
