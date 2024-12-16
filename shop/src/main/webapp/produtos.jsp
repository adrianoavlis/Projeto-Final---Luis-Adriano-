<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page import="java.util.List"%>
<%@ page import="analysis.shop.model.Produto"%>
<!DOCTYPE html>
<html lang="pt-br">

<head>
<meta charset="UTF-8">
<title>Gerenciamento de Produtos</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Argon CSS -->
<link href="assets/css/argon-dashboard.css" rel="stylesheet">
<link href="assets/css/style.css" rel="stylesheet">
<!-- Font Awesome -->
<link
	href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	rel="stylesheet">
<style>
</style>
</head>

<body>
	<!-- Sidebar -->
	<nav
		class="sidenav navbar navbar-vertical fixed-left navbar-expand-xs navbar-light bg-white shadow-sm"
		id="sidenav-main">
		<div class="scrollbar-inner">
			<!-- Logo -->
			<div class="sidenav-header align-items-center">
				<a class="navbar-brand" href="javascript:void(0)"> <img
					src="assets/img/logo-ct.png" alt="Logo" class="rounded-circle"
					style="width: 50px;">
				</a>
			</div>
			<ul class="navbar-nav">
				<li class="nav-item"><a class="nav-link" href="index.jsp">
						<i class="ni ni-shop text-primary"></i> <span>Home</span>
				</a></li>
				<li class="nav-item"><a class="nav-link"
					href="<%=request.getContextPath()%>/ProdutoController?acao=Dashboard">
						<i class="ni ni-chart-bar-32 text-warning"></i> <span>Dashboard</span>
				</a></li>
				<li class="nav-item"><a class="nav-link"
					href="<%=request.getContextPath()%>/ProdutoController?acao=Listar">
						<i class="ni ni-box-2 text-success"></i> <span>Gerenciar
							Produtos</span>
				</a></li>
			</ul>
		</div>
	</nav>

	<!-- Main Content -->
	<div class="main-content" id="panel">
		<!-- Header -->
		<div class="header bg-primary pb-6">
			<div class="container-fluid">
				<div class="header-body text-center py-6">
					<h1 class="text-white">Gerenciar Produtos</h1>
				</div>
			</div>
		</div>

		<!-- Card para adicionar produto -->
		<div class="container-fluid  mt--6">
			<div class="row py-3">
				<div class="col-md-4">
					<div class="card shadow ">
						<div class="card-body text-center">
							<i class="fas fa-plus fa-3x mb-3 text-success"></i>
							<h5 class="card-title">Adicionar Produto</h5>
							<p class="card-text">Cadastre novos produtos no sistema.</p>
							<a
								href="<%=request.getContextPath()%>/ProdutoController?acao=Adicionar"
								class="btn btn-success"> <i class="fas fa-arrow-right"></i>
								Adicionar Produto
							</a>
						</div>
					</div>
				</div>
			</div>

			<!-- Tabela de Produtos -->
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-header border-0">
                            <h3 class="mb-0">Lista de Produtos</h3>
                        </div>
                        <div class="table-responsive">
                            <table class="table align-items-center table-flush">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Nome</th>
                                        <th>Categoria</th>
                                        <th>Quantidade em Estoque</th>
                                        <th>Ações</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <%
                                    List<Produto> produtos = (List<Produto>) request.getAttribute("listaProdutos");
                                    if (produtos != null) {
                                        for (Produto produto : produtos) {
                                    %>
                                    <tr>
                                        <td><%= produto.getId() %></td>
                                        <td><%= produto.getNome() %></td>
                                        <td><%= produto.getCategoria() %></td>
                                        <td><%= produto.getQuantidadeEmEstoque() %></td>
                                        <td>
                                            <a href="<%=request.getContextPath()%>/ProdutoController?acao=Alterar&id=<%=produto.getId()%>">Editar</a>
                                            <a href="<%=request.getContextPath()%>/ProdutoController?acao=Excluir&id=<%=produto.getId()%>">Excluir</a>
                                        </td>
                                    </tr>
                                    <%
                                        }
                                    } else {
                                    %>
                                    <tr>
                                        <td colspan="5">Nenhum produto encontrado.</td>
                                    </tr>
                                    <%
                                    }
                                    %>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

		</div>
		<!-- Footer -->
		<footer class="footer pt-0">
			<div class="row align-items-center justify-content-between">
				<div class="col-lg-6 text-center text-lg-start">
					<p class="text-muted small mb-0">
						&copy; 2024 <a href="#" class="text-primary">Gerenciador de
							Produtos</a>. Todos os direitos reservados.
					</p>
				</div>
			</div>
		</footer>
	</div>

	<!-- Scripts -->
	<script src="assets/js/argon-dashboard.min.js"></script>
</body>

</html>
