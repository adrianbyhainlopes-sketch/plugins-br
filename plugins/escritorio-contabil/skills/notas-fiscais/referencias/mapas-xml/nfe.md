# Mapa de XML: NF-e e NFC-e

Fonte: Manual de Orientação do Contribuinte, versão 7.00, Anexo I, "Leiaute e Regras de Validação da NF-e e da NFC-e" (novembro de 2020, confaz.fazenda.gov.br, lido em 08/11/2026). Notas técnicas posteriores podem ter acrescentado campos, inclusive os grupos de IBS e CBS: **não conferidas aqui**. Campo que não está neste mapa não é desconhecido pelo fisco; é só não mapeado.

| Grupo | Tag | O que é |
|---|---|---|
| raiz | `infNFe`, atributo `Id` | `NFe` + chave de acesso de 44 posições |
| `ide` | `mod` | modelo: 55 NF-e, 65 NFC-e |
| `ide` | `serie`, `nNF`, `dhEmi` | série, número, data e hora |
| `ide` | `tpNF` | 0 entrada, 1 saída |
| `ide` | `cDV` | dígito da chave, módulo 11 |
| `emit` | `CNPJ` ou `CPF`, `xNome`, `IE`, `CRT` | emitente; CRT é o regime |
| `dest` | `CNPJ` ou `CPF`, `xNome` | destinatário |
| `det` (atributo `nItem`), `prod` | `cProd`, `xProd`, `NCM`, `CFOP`, `qCom`, `vUnCom`, `vProd`, `indTot` | item; `indTot` 1 compõe o total |
| `det`, `imposto`, `ICMS` | `orig`, `CST` ou `CSOSN`, `vBC`, `pICMS`, `vICMS` | grupo muda conforme CST ou CSOSN |
| `det`, `imposto` | `IPI`, `PIS`, `COFINS` | quando existem |
| `total`, `ICMSTot` | `vBC`, `vICMS`, `vICMSDeson`, `vST`, `vFCPST`, `vProd`, `vFrete`, `vSeg`, `vDesc`, `vII`, `vIPI`, `vIPIDevol`, `vPIS`, `vCOFINS`, `vOutro`, `vNF`, `vTotTrib` | totais |
| `total`, `ISSQNtot` | `vServ` | serviços na nota, quando existir |
| `infProt` | `chNFe`, `nProt`, `cStat` | protocolo; `cStat` 100 é autorizado |

## Regra do total (W16)
`vNF` = `vProd` − `vDesc` − `vICMSDeson` + `vST` + `vFCPST` + `vFrete` + `vSeg` + `vOutro` + `vII` + `vIPI` + `vIPIDevol` + `vServ`.

O manual prevê exceção para faturamento direto de veículo novo (`tpOp` igual a 2): não conferida pelo programa, que avisa.

## Chave de acesso
44 posições, a última é o dígito por módulo 11 (campo `cDV`). A chave fica como texto.

## Evento
Cancelamento e outros eventos vêm em XML separado (`infEvento`, `descEvento`). Uma nota com evento de cancelamento no lote sai dos totais; sem o evento no lote, a nota conta como válida e isso é dito.

## Armadilhas
- Item com `indTot` 0 não compõe o total.
- Grupo de ICMS muda por CST: procure o primeiro filho de `ICMS`, não um nome fixo.
- CFOP de entrada e saída vêm da nota, sem inferência.
- Quantidade × unitário pode diferir por arredondamento: o programa só avisa acima de R$ 0,01.
