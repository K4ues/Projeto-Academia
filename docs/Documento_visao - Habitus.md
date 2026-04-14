
# Documento de visão

### Histórico da Revisão 
|  Data  | Versão | Descrição | Autor |
|:-------|:-------|:----------|:------|
| 02/06/2025 | **1.1** | Criação do documento | Time Habitus |
| 25/09/2025 | **1.2** | Adição do requisitos funcionais e não-funcionais | Micael Fereira Dantas |

## 1. Objetivo do Projeto 
**Projeto**: "Habitus", aplicativo para monitoramento e controle de treinos feito para os servidores que frequentam a academia do CNAT.

## 2. Descrição do problema 
| | |
|:-|:-|
| **_O problema_** | Forma antiquada e pouco prática de registrar rotina de treino na academia do CNAT. |
| **_afetando_** | Alunos e instrutores da academia. |
| **_cujo impacto é_**| Perda de tempo, dificuldade de organização e maior chance de erros no acompanhamento dos alunos. |
| **_uma boa solução seria_** | Criação de uma plataforma que torna todo o processo menos cansativo e mais proficiente. |


## 3. Descrição dos usuários
| Nome | Descrição | Responsabilidades |
|:- |:- |:- |
| Administrador | Gestor da plataforma | Este usuário deve ser responsável pelo gerenciamento de notícias e de professores, além de monitoramento sobre o sistema em um geral. |
| Professor | Tem o papel de instrutor da academia | Este usuário pode gerenciar notícias, acessar o perfil de seus alunos, registrar, editar e excluir exercícios, além de montar rotinas de treino. Atua como um usuário híbrido, com funções de administrador e instrutor. |
| Servidor | Atua como aluno na academia. | Este usuário deve ser capaz de acessar seu próprio perfil e gerenciá-lo, junto a seus dados. Deve ser capaz de acessar seu histórico e solicitar novos treinos ao professor; Deve ser capaz também de montar e gerenciar seus próprios treinos, além de monitorar o próprio progresso. |

## 4. Descrição do ambiente dos usuários 
O aplicativo possui três tipos de usuários: administrador, professor e aluno (servidor). Todos precisam estar cadastrados e logados para acessar suas funções. O administrador gerencia o sistema, os professores e as notícias. O professor tem funções administrativas e pedagógicas, como controle de treinos, alunos e exercícios. O aluno pode gerenciar seus treinos, acompanhar seu progresso e acessar funcionalidades básicas, como feed e configurações.

## 5. Principais necessidades dos usuários
Do ponto de vista do administrador, a principal necessidade é garantir o funcionamento do sistema e manter o controle sobre professores e conteúdos. Já os professores e alunos desejam uma interface amigável que permita acompanhar treinos e progresso com mais praticidade, substituindo o método manual de fichas.

## 6. Alternativas concorrentes
**Nike Training Club**

  Pontos fortes: O app oferece treinos guiados de alta qualidade, com vídeos e planos completos elaborados por profissionais. É gratuito, bem produzido e cobre diferentes níveis de condicionamento e objetivos.
  
  Pontos fracos: Falta personalização para rotinas de musculação em academia, não permite integração com ficha de treino, e seu foco é mais voltado ao treino funcional e em casa.

**Gym WP**

  Pontos fortes: O Gym WP oferece treinos personalizados, uma ampla biblioteca de exercícios ilustrados e recursos para monitorar o progresso físico, como gráficos e controle de cansaço muscular. A interface é intuitiva e o app tem boa avaliação nas lojas.
  
  Pontos fracos: Alguns recursos importantes são pagos, o app possui poucas funcionalidades sociais e há relatos de incompatibilidade em certos dispositivos, o que pode afetar a experiência de uso.
  
**Smart Fit App**

  Pontos fortes: Permite check-in digital, reserva de aulas e acesso à ficha de treino diretamente pelo app, integrando bem com a infraestrutura da rede Smart Fit. A experiência é prática e pensada para o aluno..
  
  Pontos fracos: Assim como muitos outros aplicativos de academia ele funciona apenas para alunos da rede, tem recursos limitados para personalização dos treinos e alguns usuários relatam falhas técnicas ou lentidão no app.


## 7.	Visão geral do produto
Este projeto consiste em um aplicativo para monitoramento da rotina de treinos, com o objetivo de substituir o atual processo manual de preenchimento de fichas na academia de servidores do CNAT. O app será completo e intuitivo, proporcionando uma experiência eficiente tanto para instrutores quanto para alunos, tornando o momento de exercício físico mais proveitoso e organizado.

## 8. Requisitos Funcionais

| Código | Nome | Descrição |
|:---  |:--- |:--- |
| RF01 | Criar conta |  O usuário Aluno poderá criar uma conta no sistema. Cada usuário deve possuir apenas uma conta. |
| RF02 | Entrar no sistema | O usuário (Aluno, Professor ou Admin), após criar a conta, poderá realizar login no sistema. |
| RF03 | Sair do sistema | O usuário (Aluno, Professor ou Admin) poderá sair do sistema após estar logado.|
| RF04 | Cadastrar professor | O usuário Admin pode cadastrar novos professores no sistema.|
| RF05 | Gerenciar professores | O usuário Admin pode visualizar, editar e inativar contas de professores.|
| RF06 | Cadastrar exercício | O usuário Admin pode cadastrar novos exercícios no sistema.|
| RF07 | Gerenciar exercícios | O usuário Admin pode visualizar, editar e excluir exercícios do sistema.|
| RF08 | Publicar notícia | O usuário Admin e o Professor podem publicar notícias no sistema.|
| RF09 | Gerenciar notícias | O usuário Admin pode visualizar, editar e excluir todas as notícias. O Professor pode visualizar, editar e excluir apenas as suas próprias notícias.|
| RF10 | Adicionar novo treino | O usuário Admin, Professor ou Aluno pode adicionar novos treinos para sua própria conta.|
| RF11 | Gerenciar treinos de alunos | O usuário Professor pode visualizar, cadastrar, editar e excluir treinos de seus alunos.|
| RF12 | Adicionar aluno | O usuário Professor pode adicionar novos alunos ao sistema.|
| RF13 | Gerenciar alunos | O usuário Professor pode visualizar, editar e/ou excluir contas de alunos.|
| RF14 | Gerenciar treinos | O usuário Admin, Professor ou Aluno pode visualizar, editar e excluir seus próprios treinos.|
| RF15 | Solicitar novo treino | O usuário Aluno pode solicitar novos treinos aos professores no sistema.|
| RF16 | Zerar progresso | O usuário Admin, Professor ou Aluno pode zerar seu progresso de treino e iniciar um novo ciclo.|
| RF17 | Apagar todos os treinos | O usuário Admin, Professor ou Aluno pode apagar todos os seus treinos cadastrados no sistema.|
| RF18 | Finalizar treino | O usuário Admin, Professor ou Aluno, após terminar seu treino, poderá finalizá-lo no sistema.|


## 9. Requisitos Não-funcionais

 Código | Nome | Descrição | Categoria | Classificação
|:---  |:--- |:--- |:--- |:--- |
| RNF01 | Dados pessoais | Os usuários não podem visualizar dados pessoais de outros usuários | Privacidade | Obrigatório |
| RNF02 | Tempo de resposta | A comunicação entre o servidor e o cliente não pode ser de forma demorada | Performance | Desejável |
| RNF03 | Sistema Web Mobile | A aplicação deve ser um site Mobile | Arquitetura | Obrigatório |
| RNF04 | Controle de acesso | Só usuários autenticados (professor e admin) podem ter acesso ao sistema | Segurança | Obrigatório |
| RNF05 | Criptografia de dados| Senhas de usuários devem ser gravadas de forma criptografada no banco de dados | Segurança | Obrigatório |
