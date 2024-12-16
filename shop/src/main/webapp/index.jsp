<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-br">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análise de Produtos</title>

<link rel="stylesheet" href="assets/css/argon-dashboard.css">
<link rel="stylesheet" href="assets/css/style.css">
<!-- Font Awesome -->
<link
	href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	rel="stylesheet">
<style>
</style>
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
					href="<%=request.getContextPath()%>/ProdutoController?acao=Listar">
						<i class="ni ni-archive-2 text-success"></i> <span>Gerenciar
							Produtos</span>
				</a></li>
				<li class="nav-item"><a class="nav-link"
					href="<%=request.getContextPath()%>/ProdutoController?acao=Dashboard">
						<i class="ni ni-chart-bar-32 text-warning"></i> <span>Dashboard</span>
				</a></li>
				<li class="nav-item"><a class="nav-link"
					href="<%=request.getContextPath()%>/ProdutoController?acao=Projeto">
						<i class="ni ni-chart-bar-32 text-warning"></i> <span>O
							Projeto</span>
				</a></li>
			</ul>
		</div>
	</nav>


	<div class="main-content" id="panel">

		<div class="header bg-primary pb-6">
			<div class="container-fluid">
				<div class="header-body text-center py-6">
					<h1 class="text-white">Análise de Produtos</h1>
				</div>
			</div>
		</div>


		<div class="container-fluid mt-6">
			<div class="row">

				<div class="col-md-4">
					<div class="card shadow">
						<div class="card-body text-center">
							<i class="fas fa-list fa-3x mb-3 text-primary"></i>
							<h5 class="card-title">Listar Produtos</h5>
							<p class="card-text">Veja todos os produtos cadastrados no
								sistema.</p>
							<a
								href="<%=request.getContextPath()%>/ProdutoController?acao=Listar"
								class="btn btn-primary"> <i class="fas fa-arrow-right"></i>
								Acessar
							</a>
						</div>
					</div>
				</div>


				<div class="col-md-4">
					<div class="card shadow">
						<div class="card-body text-center">
							<i class="fas fa-chart-bar fa-3x mb-3 text-warning"></i>
							<h5 class="card-title">Dashboard</h5>
							<p class="card-text">Acompanhe estatísticas e gráficos sobre
								seus produtos.</p>
							<a
								href="<%=request.getContextPath()%>/ProdutoController?acao=Dashboard"
								class="btn btn-warning"> <i class="fas fa-arrow-right"></i>
								Acessar
							</a>
						</div>
					</div>
				</div>


				<div class="col-md-4">
					<div class="card shadow">
						<div class="card-body text-center">
							<i class="fas fa-plus fa-3x mb-3 text-success"></i>
							<h5 class="card-title">Adicionar Produtos</h5>
							<p class="card-text">Cadastre novos produtos no sistema.</p>
							<a
								href="<%=request.getContextPath()%>/ProdutoController?acao=Adicionar"
								class="btn btn-success"> <i class="fas fa-arrow-right"></i>
								Acessar
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>


	<script src="assets/js/argon-dashboard.min.js"></script>

	<script
		src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
