# Redirecionamento de URLs antigas

## Objetivo

Garantir que visitantes que acessarem URLs antigas do WooCommerce — produtos,
loja, blog ou páginas institucionais — cheguem à landing page de encerramento,
em vez de encontrarem uma página vazia ou um erro sem orientação.

## Contexto confirmado

- O site publicado é uma landing page estática no GitHub Pages.
- O repositório não possui arquivos correspondentes às rotas antigas.
- O sitemap antigo contém 125 URLs de produtos, além de outras páginas do
  WordPress/WooCommerce.
- O GitHub Pages permite uma página estática `404.html`, mas não oferece regras
  de servidor para emitir um `301` por caminho arbitrário.

## Desenho aprovado

1. Adicionar `404.html` na raiz do site.
   - Redirecionar imediatamente qualquer rota inexistente para `/`.
   - Usar `window.location.replace` para não deixar a URL antiga no histórico.
   - Incluir `meta refresh` e um link visível como fallback quando JavaScript
     estiver indisponível.
   - Marcar a página como `noindex` para evitar indexação do fallback.
2. Adicionar `sitemap.xml` com somente a URL canônica da landing page:
   `https://www.60hz.com.br/`.
3. Adicionar `robots.txt` permitindo a landing page e apontando para o sitemap.
4. Adicionar `link rel="canonical"` à `index.html`.
5. Cobrir o comportamento com testes de conteúdo e de configuração.

## Fluxo

```text
URL antiga -> GitHub Pages não encontra arquivo -> 404.html
          -> redirect para https://www.60hz.com.br/
URL canônica -> index.html -> sitemap.xml / robots.txt
```

## Limitação conhecida

O fallback atende visitantes, mas a resposta inicial continua sendo um `404`
do GitHub Pages antes do redirecionamento no navegador. Para preservar SEO com
redirecionamentos HTTP `301` reais, será necessário adicionar uma camada de
redirecionamento no Cloudflare ou no servidor anterior.

## Verificação

- Testes locais devem confirmar os arquivos, o destino canônico e a ausência de
  URLs de produtos no sitemap.
- Após publicação, verificar uma rota antiga de produto e uma rota antiga de
  página, além da landing page e do sitemap no domínio personalizado.
