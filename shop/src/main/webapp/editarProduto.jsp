<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="analysis.shop.model.Produto" %>
<%@ page import="java.util.List" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Produto</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <h1>Editar Produto</h1>
    <%
        Produto produto = (Produto) request.getAttribute("produto");
    %>
    <form action="atualizarProduto" method="post">
        <input type="hidden" name="id" value="<%= produto.getId() %>">
        Nome: <input type="text" name="nome" value="<%= produto.getNome() %>" required><br>
        Descrição: <textarea name="descricao" required><%= produto.getDescricao() %></textarea><br>
        Categoria: <input type="text" name="categoria" value="<%= produto.getCategoria() %>" required><br>
        Preço: <input type="number" name="preco" value="<%= produto.getPreco() %>" step="0.01" required><br>
        SKU: <input type="text" name="sku" value="<%= produto.getSku() %>" required><br>
        Quantidade em Estoque: <input type="number" name="quantidadeEmEstoque" value="<%= produto.getQuantidadeEmEstoque() %>" required><br>
        <input type="submit" value="Atualizar Produto">
    </form>
</body>
</html>
