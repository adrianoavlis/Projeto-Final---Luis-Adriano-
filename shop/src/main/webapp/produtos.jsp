<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.util.List" %>
<%@ page import="analysis.shop.model.Produto" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gerenciamento de Produtos</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <h1>Lista de Produtos</h1>
    
    <form action="produtos" method="post">
        <h2>Adicionar Novo Produto</h2>
        ID: <input type="text" name="id" required><br>
        Nome: <input type="text" name="nome" required><br>
        Descrição: <textarea name="descricao" required></textarea><br>
        Categoria: <input type="text" name="categoria" required><br>
        Preço: <input type="number" name="preco" step="0.01" required><br>
        SKU: <input type="text" name="sku" required><br>
        Quantidade em Estoque: <input type="number" name="quantidadeEmEstoque" required><br>
        <input type="submit" value="Adicionar Produto">
    </form>

    <h2>Produtos Cadastrados</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Descrição</th>
            <th>Categoria</th>
            <th>Preço</th>
            <th>SKU</th>
            <th>Quantidade em Estoque</th>
            <th>Ações</th>
        </tr>
        <%
            List<Produto> produtos = (List<Produto>) request.getAttribute("produtos");
            if (produtos != null) {
                for (Produto produto : produtos) {
        %>
        <tr>
            <td><%= produto.getId() %></td>
            <td><%= produto.getNome() %></td>
            <td><%= produto.getDescricao() %></td>
            <td><%= produto.getCategoria() %></td>
            <td><%= produto.getPreco() %></td>
            <td><%= produto.getSku() %></td>
            <td><%= produto.getQuantidadeEmEstoque() %></td>
            <td>
                <a href="editarProduto?id=<%= produto.getId() %>">Editar</a>
                <a href="deletarProduto?id=<%= produto.getId() %>" onclick="return confirm('Tem certeza que deseja excluir?');">Excluir</a>
            </td>
        </tr>
        <%
                }
            } else {
        %>
        <tr>
            <td colspan="8">Nenhum produto encontrado.</td>
        </tr>
        <%
            }
        %>
    </table>
</body>
</html>
