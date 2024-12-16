<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page import="analysis.shop.model.Produto"%>
<%@ page import="java.util.List"%>
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Editar Produto</title>

<link rel="stylesheet" href="assets/css/argon-dashboard.css">
<link rel="stylesheet" href="assets/css/style.css">

<link
	href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	rel="stylesheet">
</head>
<body>
	<nav
		class="sidenav navbar navbar-vertical fixed-left navbar-expand-xs navbar-light bg-white shadow-sm"
		id="sidenav-main">
		<div class="scrollbar-inner">

			<div class="sidenav-header align-items-center">
				<a class="navbar-brand" href="javascript:void(0)"> <img
					src="assets/img/LOGO.png" alt="Logo" class="rounded-circle"
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

			</ul>
		</div>
	</nav>
	<%
	Produto produto = (Produto) request.getAttribute("produto");
	%>
	<div class="main-content" id="panel">
		<div class="header bg-primary pb-6">
			<div class="container-fluid">
				<div class="header-body text-center py-6">
					<h1 class="text-white">Editar Produto</h1>
				</div>
			</div>
		</div>

		<div class="container-fluid mt--6">

			<div class="row">
				<div class="col">
					<div class="card">
						<div class="card-header">
							<h3 class="mb-0">Editar Produto</h3>
						</div>
						<div class="card-body">
							<form action="<%=request.getContextPath()%>/ProdutoController"
								method="post">
								<input type="hidden" name="id" value="<%=produto.getId()%>" />

								<div class="form-group">
									<label for="nome">Nome:</label> <input type="text"
										class="form-control" id="nome" name="nome"
										value="<%=produto.getNome()%>" required>
								</div>

								<div class="form-group">
									<label for="descricao">Descrição:</label>
									<textarea class="form-control" id="descricao" name="descricao"
										required><%=produto.getDescricao()%></textarea>
								</div>

								<div class="form-group">
									<label for="categoria">Categoria:</label> <input type="text"
										class="form-control" id="categoria" name="categoria"
										value="<%=produto.getCategoria()%>" required>
								</div>

								<div class="form-group">
									<label for="preco">Preço:</label> <input type="number"
										class="form-control" id="preco" name="preco"
										value="<%=produto.getPreco()%>" step="0.01" required>
								</div>

								<div class="form-group">
									<label for="sku">SKU:</label> <input type="text"
										class="form-control" id="sku" name="sku"
										value="<%=produto.getSku()%>" required>
								</div>

								<div class="form-group">
									<label for="quantidadeEmEstoque">Quantidade em Estoque:</label>
									<input type="number" class="form-control"
										id="quantidadeEmEstoque" name="quantidadeEmEstoque"
										value="<%=produto.getQuantidadeEmEstoque()%>" required>
								</div>

								<button type="submit" class="btn btn-primary">Atualizar
									Produto</button>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>

	</div>
</body>
</html>
