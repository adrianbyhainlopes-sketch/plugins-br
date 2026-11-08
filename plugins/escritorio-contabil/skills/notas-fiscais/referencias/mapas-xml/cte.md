# Mapa de XML: CT-e

**Mapa não conferido no manual oficial do CT-e:** foi escrito pela semelhança com a NF-e e testado só com arquivo sintético. Compare com um XML real antes de confiar nas somas, e diga isso no relatório.

| Grupo | Tag | O que é |
|---|---|---|
| raiz | `infCte`, atributo `Id` | `CTe` + chave |
| `ide` | `CFOP`, `natOp`, `serie`, `nCT`, `dhEmi` | identificação |
| `emit` | `CNPJ`, `xNome` | transportador |
| `vPrest` | `vTPrest`, `vRec`, `Comp` (`xNome`, `vComp`) | valor da prestação e componentes |
| `imp`, `ICMS` | `CST`, `vBC`, `pICMS`, `vICMS` | imposto |
| `infProt` | `nProt`, `cStat` | protocolo |

Conferência feita: componentes somam `vTPrest`; dígito da chave; protocolo.
