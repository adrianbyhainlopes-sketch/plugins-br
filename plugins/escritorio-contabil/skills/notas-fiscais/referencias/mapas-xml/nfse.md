# Mapa de XML: NFS-e

## Padrão nacional
Fonte: Anexo I, leiaute DPS e NFS-e, versão 1.01 de 09/02/2026, gov.br/nfse (documentação atual, lido em 08/11/2026). A própria página avisa que parte da documentação é minuta.

| Caminho | Tag | O que é |
|---|---|---|
| `NFSe/infNFSe` | `nNFSe` | número |
| `NFSe/infNFSe` | `cStat` | 100 gerada; 102 decisão judicial ou administrativa; 103 avulsa; 107 MEI |
| `NFSe/infNFSe/emit` | `CNPJ` ou `CPF`, `xNome` | emitente |
| `NFSe/infNFSe/valores` | `vBC`, `pAliqAplic`, `vISSQN`, `vTotalRet`, `vLiq` | valores da nota |
| `.../DPS/infDPS` | `dhEmi` | emissão |
| `.../infDPS/toma` | `CNPJ` ou `CPF`, `xNome` | tomador |
| `.../infDPS/serv/cServ` | `cTribNac`, `xDescServ` | serviço |
| `.../infDPS/valores/vServPrest` | `vServ` | valor do serviço |
| `.../infDPS/valores/trib/tribMun` | `tribISSQN` (1 tributável; 2 imunidade; 3 exportação; 4 não incidência), `tpRetISSQN` (1 não retido; 2 retido pelo tomador; 3 pelo intermediário), `pAliq` | ISS |

Identidades do leiaute: `vBC` = serviço − desconto incondicionado − deduções − benefício municipal; `vLiq` = serviço − desconto condicionado − desconto incondicionado − valores retidos (o programa usa `vTotalRet`). CP, IRRF e CSLL são sempre subtraídos, se constarem; ISSQN, PIS e Cofins só quando retidos.

## Leiaute municipal
Muitas prefeituras têm leiaute próprio, fora do padrão nacional (por exemplo, com as tags `CompNfse` e `InfNfse`). O programa conta esses arquivos, lista à parte e não soma. Para incluir: peça um XML real ou o manual da prefeitura, escreva o mapa aqui nesse mesmo formato e confira contra a soma das notas.
