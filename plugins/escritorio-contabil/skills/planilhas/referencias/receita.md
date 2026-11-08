# Receita reutilizável e repetição mensal

Uma receita descreve como tratar uma exportação, sem nenhum dado dela. Guarde em JSON, ao lado do trabalho do cliente.

## Formato
```json
{
  "versao": 3,
  "nome": "exportacao-contas-a-pagar",
  "significado_da_linha": "um título a pagar",
  "entradas": [{"papel": "contas_a_pagar", "abas": ["Planilha1"], "codificacao": "cp1252", "delimitador": ";"}],
  "colunas": [
    {"origem": "CNPJ Fornecedor", "destino": "fornecedor_cnpj", "tipo": "texto"},
    {"origem": "Vencimento", "destino": "vencimento", "tipo": "data", "formato": "%d/%m/%Y"},
    {"origem": "Valor", "destino": "valor", "tipo": "dinheiro", "decimal": "virgula"}
  ],
  "chaves": {"principal": ["documento"], "padrao_de_juncao": "1 para 1"},
  "regras": {"valor_vazio": "pendência", "duplicata": "mesma chave e mesmo valor, a confirmar", "exclusoes": []},
  "saida": {"formato": "csv", "delimitador": ";", "codificacao": "utf-8-sig"},
  "verificacoes": ["soma do valor antes = depois", "registros = contribuíram + pendentes + excluídos"],
  "historico_de_entradas": [{"nome": "maio.csv", "hash_sha256": "...", "abas": ["Planilha1"], "competencia": "2026-05", "decisao": "acrescenta"}],
  "decisoes_por_linha": []
}
```

Decisões por linha ficam separadas das regras gerais. A receita não guarda nome de cliente, CNPJ nem valor do arquivo de exemplo.

## Repetir
1. Compare o arquivo novo com a receita: cabeçalhos, abas, significado das colunas e da linha, tipos, configuração regional, chaves, unidades.
2. Coluna renomeada ou nova é sinalizada, nunca mapeada por palpite (`client_id` para `client_code` pode não ser a mesma coisa). Pause só o que depende do problema e siga com o resto.
3. **Mesma entrada duas vezes:** calcule o hash do conteúdo e confira no histórico. Nome de arquivo ou número de linha não provam igualdade. Não some duas vezes o mesmo arquivo. Pergunte se o arquivo novo **substitui** o período ou **acrescenta** registros, sem deduzir pelo nome.
4. Decisão sobre linha antiga nunca é aplicada automaticamente a linha nova.
5. Saídas sempre em local novo. Nunca sobrescreva entradas nem resultados anteriores.
6. **Teste de repetibilidade:** rode de novo numa saída de rascunho; entradas e regras iguais dão os mesmos registros e decisões, sem criar entrada nova no histórico.
7. Recalcule contagens e totais finais com a fórmula e as entradas reais. Mudança de contagem não prova causa.

Devolva primeiro os arquivos, depois as diferenças relevantes e uma decisão necessária. Não prometa agendamento nem atualização automática.
