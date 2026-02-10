const supabase = supabasejs.createClient(
  "SUA_PROJECT_URL",
  "SUA_ANON_KEY"
)

async function criarPedido() {
  const nome = document.getElementById("nome").value
  const whats = document.getElementById("whats").value
  const total = 99.90

  const { data, error } = await supabase
    .from("pedidos")
    .insert({
      cliente_nome: nome,
      whatsapp: whats,
      total: total,
      status: "aguardando_pagamento"
    })
    .select()
    .single()

  gerarPix(data.id, total)
}
