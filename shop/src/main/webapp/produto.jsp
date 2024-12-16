<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.util.List"%>
<%@ page import="analysis.shop.model.Produto"%>
<!DOCTYPE html>

<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Produtos</title>
    <!-- Argon CSS -->
    <link href="assets/css/argon-dashboard.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
    <style>
       
    </style>
</head>

<body>
    <!-- Sidebar -->
    <nav class="sidenav navbar navbar-vertical fixed-left navbar-expand-xs navbar-light bg-white shadow-sm" id="sidenav-main">
        <div class="scrollbar-inner">
            <!-- Logo -->
            <div class="sidenav-header align-items-center">
                <a class="navbar-brand" href="javascript:void(0)">
                    <img src="assets/img/logo-ct.png" alt="Logo" class="rounded-circle" style="width: 50px;">
                </a>
            </div>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="index.jsp">
                        <i class="ni ni-shop text-primary"></i>
                        <span>Home</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="<%= request.getContextPath() %>/ProdutoController?acao=Listar">
                        <i class="ni ni-shop text-primary"></i>
                        <span>Gerenciar Produtos</span>
                    </a>
                </li>
                <!-- Adicione mais links conforme necessário -->
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content" id="panel">
        <!-- Header -->
        <div class="header bg-primary pb-6">
            <div class="container-fluid">
                <div class="header-body">
                    <div class="row align-items-center py-4">
                        <div class="col-lg-6 col-7">
                            <h6 class="h2 text-white d-inline-block mb-0">Dashboard</h6>
                        </div>
                    </div>
                    <!-- Resumo -->
                    <%
                    List<Produto> produtos = (List<Produto>) request.getAttribute("listaProdutos");
                    %>
                    <div class="row">
                        <div class="col-xl-4 col-md-6">
                            <div class="total-produtos">
                                <h5 class="card-title text-uppercase text-muted mb-0">Total de Produtos</h5>
                                <span class="h2 font-weight-bold mb-0">
                                    <%= produtos != null ? produtos.size() : 0 %>
                                </span>
                            </div>
                        </div>
                        <!-- Mais cards aqui -->
                    </div>
                    
                    <div class="row">
							<%
							// Ordenar os produtos pelo preço para pegar os 4 mais baratos

							if (produtos != null && produtos.size() > 0) {
								produtos.sort((p1, p2) -> Double.compare(p1.getPreco(), p2.getPreco())); // Ordena por preço crescente
								for (int i = 0; i < Math.min(4, produtos.size()); i++) {
									Produto produto = produtos.get(i);
							%>
							<div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
								<div class="card">
									<div class="card-body p-3">
										<div class="row">
											<div class="col-8">
												<div class="numbers">
													<p class="text-sm mb-0 text-uppercase font-weight-bold">
														<%=produto.getNome()%>
													</p>
													<h5 class="font-weight-bolder">
														R$
														<%=String.format("%.2f", produto.getPreco())%>
													</h5>
													<p class="mb-0 text-muted">Produto mais barato</p>
												</div>
											</div>
											<div class="col-4 text-end">
												<div
													class="icon icon-shape bg-gradient-info shadow-info text-center rounded-circle">
													<i class="ni ni-tag text-lg opacity-10" aria-hidden="true"></i>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<%
							}
							} else {
							%>
							<div class="col-12">
								<div class="alert alert-warning" role="alert">Nenhum
									produto encontrado.</div>
							</div>
							<%
							}
							%>
						</div>
                </div>
            </div>
        </div>

        <!-- Content -->
        <div class="container-fluid mt--6">
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
                                    </tr>
                                </thead>
                                <tbody>
                                    <%
                                    if (produtos != null) {
                                        for (Produto produto : produtos) {
                                    %>
                                    <tr>
                                        <td><%= produto.getId() %></td>
                                        <td><%= produto.getNome() %></td>
                                        <td><%= produto.getCategoria() %></td>
                                        <td><%= produto.getQuantidadeEmEstoque() %></td>
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

            <!-- Gráfico -->
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <canvas id="chart-bars"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Argon JS -->
    <script src="assets/js/argon-dashboard.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Gráfico de barras de exemplo
        var ctx = document.getElementById('chart-bars').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Categoria 1', 'Categoria 2', 'Categoria 3'], // Substituir dinamicamente
                datasets: [{
                    label: 'Quantidade',
                    data: [10, 20, 30], // Substituir dinamicamente
                    backgroundColor: 'rgba(94, 114, 228, 0.8)'
                }]
            }
        });
    </script>
</body>

</html>
