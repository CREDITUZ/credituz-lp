from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise SystemExit(f"Nao encontrado: {label}")
    text = text.replace(old, new, 1)

replace_once(
    '<h2>Dois produtos. <em>Uma infraestrutura financeira.</em></h2>',
    '<h2>Produtos para <em>decidir, financiar e receber melhor.</em></h2>',
    "titulo da secao de produtos",
)

replace_once(
    '<p class="arch-lead">Use o Credituz OS para analisar risco e receber melhor. Use o CORBAN AI para incorporar crédito à jornada do seu cliente. Combine os dois no Enterprise quando sua operação exigir mais.</p>',
    '<p class="arch-lead">Do terreno à operação financeira: use o Incorporador OS para decidir onde investir, o Credituz OS para analisar risco e receber melhor e o CORBAN AI para incorporar crédito à jornada do cliente.</p>',
    "lead da secao de produtos",
)

old_split = '    <div class="arch-split-note"><strong>Credituz OS cuida do risco e do recebimento.</strong><span>CORBAN AI cuida da originação do crédito.</span></div>'
incorporador = '''    <article class="inc-os-card" id="incorporador-os">
      <div class="inc-os-copy">
        <div class="arch-product-top"><span class="arch-product-label">Incorporador OS</span><span class="arch-product-price arch-product-price-small">Viabilidade imobiliária</span></div>
        <h3>Da análise do terreno à decisão de investimento, toda a viabilidade do empreendimento em um só lugar.</h3>
        <p>Simule cenários, analise VGV, margem, TIR, fluxo de caixa, exposição de capital e distribuição de resultados com memória de cálculo e inteligência para tomada de decisão.</p>
        <div class="arch-flow"><span>Terreno</span><i>→</i><span>Viabilidade</span><i>→</i><span>Cenários</span><i>→</i><span>Decisão</span></div>
        <ul class="arch-list">
          <li>VGV, margem, TIR, VPL e exposição de caixa</li>
          <li>Cenários e análise de sensibilidade</li>
          <li>Estrutura de capital e distribuição de resultados</li>
          <li>Memória de cálculo e parecer de viabilidade</li>
        </ul>
        <a class="arch-btn" href="https://viabilidade.credituz.ai/" target="_blank" rel="noopener" data-track="cta_product_incorporador">Conhecer Incorporador OS</a>
        <span class="inc-os-note">Planos, preços e funcionalidades completas ficam na página do produto.</span>
      </div>
      <a class="inc-os-visual" href="https://viabilidade.credituz.ai/" target="_blank" rel="noopener" aria-label="Conhecer Incorporador OS">
        <img src="/assets/incorporador-os-waterfall.webp" width="426" height="430" loading="lazy" alt="Tela ilustrativa do Incorporador OS com cascata de distribuição e retorno de sócios">
      </a>
    </article>
    <div class="arch-split-note"><strong>Incorporador OS ajuda a decidir onde investir.</strong><span>Credituz OS cuida do risco e do recebimento.</span><span>CORBAN AI cuida da originação do crédito.</span></div>'''
replace_once(old_split, incorporador, "resumo dos produtos")

score_marker = "<!-- SCORE -->"
journey = '''<!-- ECOSSISTEMA -->
<section class="arch-section arch-journey" id="ecossistema">
  <div class="arch-inner">
    <div class="section-tag">Ecossistema Credituz</div>
    <h2>Tecnologia para <em>toda a jornada imobiliária.</em></h2>
    <p class="arch-lead">Da análise do terreno ao recebimento da última parcela, a Credituz conecta viabilidade, crédito, financiamento e cobrança em um só ecossistema.</p>
    <div class="journey-flow" aria-label="Jornada imobiliária Credituz">
      <span>Terreno</span><i>→</i><span>Viabilidade</span><i>→</i><span>Venda</span><i>→</i><span>Análise de crédito</span><i>→</i><span>Financiamento</span><i>→</i><span>Cobrança e recebíveis</span>
    </div>
  </div>
</section>

<!-- SCORE -->'''
replace_once(score_marker, journey, "marcador da secao Score")

styles = '''<style id="home-incorporador-os-v1">
.inc-os-card{margin-top:18px;display:grid;grid-template-columns:minmax(0,1fr) minmax(320px,.78fr);gap:34px;align-items:center;padding:34px;border:1px solid #252b38;border-radius:26px;background:#090b10;color:#fff;overflow:hidden}.inc-os-card .arch-product-label{color:var(--accent-bright)}.inc-os-card .arch-product-price-small{color:#a7a7ad}.inc-os-card h3{font-size:clamp(29px,3.6vw,44px);margin:20px 0 14px;max-width:720px}.inc-os-card p,.inc-os-card li{color:#c7c7cc}.inc-os-card .arch-flow{background:#151821;color:#fff}.inc-os-card .arch-list li:before{color:#69b4ff}.inc-os-card .arch-btn{background:#fff;color:#111;border-color:#fff}.inc-os-note{display:block;margin-top:12px;color:#8e8e93;font-size:12.5px}.inc-os-visual{display:block;text-decoration:none}.inc-os-visual img{display:block;width:100%;height:auto;border:1px solid #252b38;border-radius:20px;background:#0d0f14}.arch-journey{padding-top:70px;padding-bottom:70px;background:var(--paper-warm);border-top:1px solid var(--gray-soft);border-bottom:1px solid var(--gray-soft)}.arch-journey .arch-lead{margin-bottom:26px}.journey-flow{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.journey-flow span{padding:11px 15px;border:1px solid var(--gray-soft);border-radius:999px;background:#fff;font-size:14px;font-weight:700}.journey-flow i{font-style:normal;color:var(--gray-3)}
@media(max-width:820px){.inc-os-card{grid-template-columns:1fr;padding:24px}.inc-os-visual{max-width:520px}.journey-flow{align-items:flex-start}.journey-flow i{padding-top:10px}}
</style>
'''
clarity_marker = "<!-- Microsoft Clarity -->"
if "home-incorporador-os-v1" not in text:
    replace_once(clarity_marker, styles + clarity_marker, "marcador de estilos")

path.write_text(text, encoding="utf-8")
