# Implementation Contract v1

Sua resposta será processada automaticamente por outro sistema.

Qualquer divergência deste contrato tornará a resposta inválida.

## Regras Gerais

- Retorne exclusivamente um JSON válido.
- Nunca utilize Markdown.
- Nunca utilize blocos ```json.
- Nunca escreva explicações.
- Nunca escreva comentários.
- Nunca escreva texto antes ou depois do JSON.
- Sempre gere arquivos completos.
- Nunca gere snippets.
- Nunca omita arquivos da tarefa.
- Nunca altere arquivos que não estejam presentes na tarefa.

## Estrutura Obrigatória

```json
{
    "generated_files": [
        {
            "path": "",
            "content": ""
        }
    ]
}
```

## Regras dos Campos

### generated_files

Lista contendo todos os arquivos gerados para esta tarefa.

### path

- Caminho relativo do arquivo.
- Deve ser exatamente o caminho existente no repositório.

Exemplo:

```
src/Stellantis.Finance.Dealer.Api/Program.cs
```

### content

Deve conter:

- O arquivo completo.
- Código compilável.
- Resultado final da integração.
- Preservando alterações existentes da branch destino que não estejam relacionadas à branch origem.

Nunca retorne apenas o trecho alterado.

## Validação Final

Antes de finalizar sua resposta, valide internamente que:

- O JSON é válido.
- Existe a propriedade `generated_files`.
- Todos os itens possuem `path`.
- Todos os itens possuem `content`.
- Todos os arquivos são completos.
- Nenhum arquivo externo à tarefa foi gerado.
- A resposta contém exclusivamente o JSON definido neste contrato.