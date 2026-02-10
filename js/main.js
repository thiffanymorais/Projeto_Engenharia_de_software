$(document).ready(function(){

    $('body').scrollspy({ target: '#cabecalho', offset:10 }); 

    $('#telefone').mask('(00) 00000-0000',{
        placeholder:'(00) 00000-00000'
    });

    $('form').validate({
        rules:{
            nome:{
                required:true
            },
            email:{
                required:true,
                email:true
            },
            mensagem:{
                required:true
            }
        },
        messages:{
            nome:'Por favor insira o seu nome!'
        },

        submitHandler: function (form){
            console.log(form);
        },

        invalidHandler: function (evento, validador){
            let camposIncorretos = validador.numberOfInvalids();
            if (camposIncorretos){
                alert (`Existem ${camposIncorretos} campos incorretos!`);
            };
        }
    });
});

document.addEventListener('DOMContentLoaded', function(){
    const modal = new bootstrap.Modal('#modal');
    setTimeout(function(){
        modal.show();
    }, 3000);
})
// ===============================
// 🛒 CARRINHO (JS PURO)
// ===============================
let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];

atualizarCarrinho();

function adicionarCarrinho(nome, preco){
    const produto = carrinho.find(p => p.nome === nome);

    if(produto){
        produto.qtd++;
    } else {
        carrinho.push({ nome, preco, qtd: 1 });
    }

    salvarCarrinho();
}

function removerItem(index){
    carrinho.splice(index, 1);
    salvarCarrinho();
}

function salvarCarrinho(){
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
    atualizarCarrinho();
}

function atualizarCarrinho(){
    const contador = document.getElementById("contadorCarrinho");
    if(contador){
        contador.innerText = carrinho.length;
    }
}

function abrirCarrinho(){
    const modal = new bootstrap.Modal(
        document.getElementById("modalCarrinho")
    );
    modal.show();
}
