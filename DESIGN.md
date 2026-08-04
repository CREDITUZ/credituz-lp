# DNA visual — `correspondente.credituz.ai`

Referência de estilo aplicada ao `credituz.ai`. Extraída de
`correspondente.credituz.ai/app/globals.css`, `components/ui/button.tsx` e das cenas
em `components/site/`.

O layout do `credituz.ai` **não muda**: só cor, tipografia, pattern e estilização.

## 1. Princípio

Página de produto no ritmo da Apple: superfícies quase brancas, uma única cor de
marca (azul) reservada para ação e ênfase, e cenas pretas usadas como corte
dramático entre blocos claros. Nada de cor quente, nada de serifa, nada de caixa
alta com tracking aberto.

## 2. Paleta

### Superfícies claras (padrão)

| Token | Valor | Uso |
|---|---|---|
| `--paper` | `#ffffff` | fundo padrão das seções |
| `--paper-warm` | `#f5f5f7` | seção alternada / fundo de card |
| `--cream` | `#e8e8ed` | chips, divisórias suaves |
| `--gray-soft` | `#d2d2d7` | borda de 1px (única espessura usada) |

### Tinta

| Token | Valor | Uso |
|---|---|---|
| `--ink` | `#1d1d1f` | texto principal e fundo das cenas escuras |
| `--gray-1` | `#1d1d1f` | títulos |
| `--gray-2` | `#6e6e73` | texto secundário |
| `--gray-3` | `#86868b` | meta, legenda, rótulo |

### Acento

| Token | Valor | Uso |
|---|---|---|
| `--lime` | `#0071e3` | **acento sólido**: fundo de botão/badge, sempre com texto branco |
| `--lime-deep` | `#0066cc` | hover do acento sólido |
| `--accent-bright` | `#6bb2ff` | acento **como texto sobre cena escura** — `#0071e3` no preto não lê |
| `--accent-soft` | `rgba(0,113,227,.10)` | fundo de badge/pill discreto, com texto `--lime` |

Os nomes `--lime`/`--lime-deep` foram mantidos para não reescrever as ~4.000 linhas
de CSS que já os consomem. O valor é azul; o nome é histórico.

### Cenas escuras

| Token | Valor | Uso |
|---|---|---|
| `--void` | `#000000` | seção de oferta / fechamento |
| `--slab` | `#0a0a0c` | fundo escuro alternativo |
| `--panel` | `#161617` | card dentro de cena escura |
| `--dark-hair` | `#2a2a2e` | borda dentro de cena escura |

Sobre preto, texto é `#f5f5f7` e o secundário `#86868b` — nunca branco puro em bloco
de parágrafo.

### Semânticos

`--good #1d9d54` · `--warn #b25000` · `--rust/--bad #b25000` · destrutivo `#d70015`.

## 3. Tipografia

Uma família só, a do sistema. Sem Google Fonts.

```css
--font-sans: ui-sans-serif, -apple-system, BlinkMacSystemFont, "SF Pro Display",
             "SF Pro Text", "Helvetica Neue", "Inter", system-ui, sans-serif;
--font-mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace;
```

Escala e ritmo — tracking negativo forte, line-height curto, peso 600:

| Papel | Tamanho | Tracking | Peso |
|---|---|---|---|
| display | `clamp(2.75rem, 7.5vw, 6.5rem)` / lh 1 | `-0.035em` | 600 |
| title (h2) | `clamp(2rem, 5vw, 3.75rem)` / lh 1.06 | `-0.03em` | 600 |
| subtitle (h3) | `clamp(1.375rem, 2.6vw, 2rem)` / lh 1.15 | `-0.022em` | 600 |
| lede | `clamp(1.06rem, 1.5vw, 1.31rem)` / lh 1.45 | `-0.01em` | 400 |
| eyebrow | `clamp(.875rem, 1.1vw, 1.06rem)` | `-0.01em` | 600 |
| corpo | 15–17px / lh 1.5 | `-0.01em` | 400 |

O eyebrow é a mudança mais visível: **sem caixa alta, sem letter-spacing aberto e
sem travessão**. É só a frase curta na cor do acento, no mesmo ritmo do resto —
não um rótulo de sistema com ornamento na frente. Números animados levam `font-variant-numeric: tabular-nums`.

Itálico não faz parte do sistema: onde havia serifa itálica de ênfase, use peso
600 na cor do acento.

## 4. Forma

- **Raio**: pill `100px` para botão/badge; `26px` para card de grade
  (`rounded-[26px]`); `16px` para chip interno; `12px` para botão retangular.
- **Card não tem contorno.** Esta é a regra que mais muda a leitura da página. A
  separação vem da **superfície**, e a superfície é sempre a oposta da seção:

  | seção | card |
  |---|---|
  | `--paper` (branco) | `--paper-warm` |
  | `--paper-warm` | `--paper` |
  | cena escura | `#141416` ou `rgba(255,255,255,.04)` |

  Em todo o correspondente há exatamente 5 declarações de borda, e todas são
  `border-t`/`border-b` — divisórias de lista (FAQ), não caixas.
- **Borda**: só como fio divisório, `1px solid var(--gray-soft)` no claro e
  `var(--dark-hair)` no escuro. Nunca 2px ou 3px, nunca contornando um card.
- **Sombra**: uma só no sistema inteiro —
  `0 1px 3px rgba(0,0,0,.08), 0 8px 24px rgba(0,0,0,.08)`. Usada onde algo
  precisa de fato flutuar (o controle sobre o aparelho no hero). Card de grade
  nunca tem sombra.
- **Halo**: cena escura pode ter um círculo de acento desfocado atrás do conteúdo —
  `background: #0071e3; opacity: .18; filter: blur(120px)`. É o único "efeito".

## 5. Botões

| Variante | Fundo | Texto |
|---|---|---|
| primária | `--lime` | `#fff` |
| preta | `--ink` | `#fff` |
| secundária | `--paper-warm` | `--ink` |
| contorno | `--paper` + borda `--gray-soft` | `--ink` |
| link | transparente | `--lime`, sublinhado no hover |

Alturas 40 / 48 / 56px, `font-weight: 600`, `letter-spacing: -0.01em`.
Hover é `scale(1.02)` ou escurecer 10% — nunca troca de cor de marca.

## 6. Movimento

Easing único: `cubic-bezier(0.22, 1, 0.36, 1)`, 250–700 ms. Entrada é
`opacity 0→1` + `translateY(12–16px)`, às vezes com `blur(6px)→0`. Nada depende de
scroll para completar: dispara ao entrar em vista e termina sozinho.
`prefers-reduced-motion` zera tudo.

## 7. A tela do produto

`PhoneApp.tsx` é um tema iOS **claro e chapado**, e é o que qualquer mockup de
produto na página deve seguir: fundo `#fafafa`, superfície `#ffffff`, fio
`#e5e5e5`, texto `#171717`, secundário `#737373`, azul `#007aff`, verde
`#34c759`, vermelho `#ff3b30`. Sem gradiente, sem sombra interna, sem cartão
escuro girado. Balão de conversa: cinza `#e9e9eb` para o cliente, `#007aff` com
texto branco para a IA, raio `18px` com o canto da ponta em `5px`. Valor sempre
com `font-variant-numeric: tabular-nums` — sem isso os números dançam na
horizontal a cada atualização.

Janela de navegador segue o Safari: semáforo, toggle de sidebar, chevrons, campo
de endereço centrado com cadeado, e share / nova aba / abas à direita. Ícones do
lucide, traço `1.7–1.8`, grid 24.

## 8. Navbar

A nav é vidro translúcido (`rgba(255,255,255,.72)` + `backdrop-filter: saturate(180%) blur(20px)`)
e **inverte quando passa sobre uma cena escura**: fundo `rgba(29,29,31,.72)`, links
`#f5f5f7`, wordmark invertida por `filter: brightness(0) invert(1)` e o CTA azul
virando pílula branca com texto `--ink`. Sem isso a faixa branca corta o preto.

Quem liga a classe `.on-dark` é um script no fim de cada página que mede a
**luminância do fundo computado** de cada `section`/`footer`/`header` e checa, a cada
frame de scroll, se alguma cena escura cruza a faixa da nav. Não há lista de seções
para manter: seção escura nova já funciona. Para forçar o estado em um elemento que
não seja seção (um card full-bleed, por exemplo), marque com `data-nav-dark`.

## 9. Ritmo da página

Alternância clara/escura é o que dá a cadência: bloco branco → bloco `#f5f5f7` →
cena preta → volta. Padding vertical de seção `clamp(6rem, 10vw, 8rem)`,
padding lateral `clamp(1.25rem, 4vw, 3.5rem)`, conteúdo em `max-width: 1180px`.
