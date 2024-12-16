<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-br">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cadastrar Produto</title>

<link rel="stylesheet" href="assets/css/argon-dashboard.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>

<body>

	<nav
		class="sidenav navbar navbar-vertical fixed-left navbar-expand-xs navbar-light bg-white shadow-sm"
		id="sidenav-main">
		<div class="scrollbar-inner">

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
					href="<%=request.getContextPath()%>/ProdutoController?acao=Listar">
						<i class="ni ni-shop text-primary"></i> <span>Gerenciar
							Produtos</span>
				</a></li>

			</ul>
		</div>
	</nav>

	<div class="main-content" id="panel" style="margin-left: 250px;">

		<div class="header bg-primary pb-6">
			<div class="container-fluid">
				<div class="header-body">
					<div class="row align-items-center py-4">
						<div class="col-lg-6 col-7">
							<h6 class="h2 text-white d-inline-block mb-0">Cadastro de
								Novo Produto</h6>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="container-fluid mt--6">
			<div class="row">
				<div class="col">
					<div class="card">
						<div class="card-header">
							<h3 class="mb-0">Cadastro de Novo Produto</h3>
						</div>
						<div class="card-body">
							<form action="<%=request.getContextPath()%>/ProdutoController"
								method="post">
								<input type="hidden" name="acao" value="Adicionar" />
								<div class="form-group">
									<label for="nome">Nome:</label> <input type="text"
										class="form-control" id="nome" name="nome" required>
								</div>
								<div class="form-group">
									<label for="descricao">Descrição:</label>
									<textarea class="form-control" id="descricao" name="descricao"
										required></textarea>
								</div>
								<div class="form-group">
									<label for="categoria">Categoria:</label> <input type="text"
										class="form-control" id="categoria" name="categoria" required>
								</div>
								<div class="form-group">
									<label for="preco">Preço:</label> <input type="number"
										class="form-control" id="preco" name="preco" step="0.01"
										required>
								</div>
								<div class="form-group">
									<label for="sku">SKU:</label> <input type="text"
										class="form-control" id="sku" name="sku" required>
								</div>
								<div class="form-group">
									<label for="quantidadeEmEstoque">Quantidade em Estoque:</label>
									<input type="number" class="form-control"
										id="quantidadeEmEstoque" name="quantidadeEmEstoque" required>
								</div>
								<button type="submit" class="btn btn-primary">Adicionar
									Produto</button>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Scripts -->
	<script src="assets/js/argon-dashboard.min.js"></script>
</body>

</html>
