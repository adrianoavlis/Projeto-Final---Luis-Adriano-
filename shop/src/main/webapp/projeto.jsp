<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto - Detalhamento</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/css/all.min.css" rel="stylesheet">

    <!-- Mermaid.js -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>

    <!-- Custom CSS -->
    <style>
        .container {
            margin-top: 20px;
        }

        .card-body {
            padding: 20px;
        }
        
        .mermaid {
            margin-top: 20px;
        }

        /* Responsividade */
        @media (max-width: 768px) {
            .mermaid {
                font-size: 14px;
            }
        }
    </style>
</head>

<body>
  <!-- Sidenav -->
    
     <nav class="sidenav navbar navbar-vertical fixed-left navbar-expand-xs navbar-light bg-white shadow-sm" id="sidenav-main">
        <div class="scrollbar-inner">
            <!-- Logo -->
            <div class="sidenav-header align-items-center">
                <a class="navbar-brand" href="javascript:void(0)">
                    <img src="assets/img/LOGO.png" alt="Logo" class="rounded-circle" style="width: 50px;">
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
                        <i class="ni ni-archive-2 text-success"></i>
                        <span>Gerenciar Produtos</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="<%= request.getContextPath() %>/ProdutoController?acao=Dashboard">
                        <i class="ni ni-chart-bar-32 text-warning"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="<%= request.getContextPath() %>/ProdutoController?acao=Projeto">
                        <i class="ni ni-chart-bar-32 text-warning"></i>
                        <span>O Projeto</span>
                    </a>
                </li>
                <!-- Adicione mais links conforme necessário -->
            </ul>
        </div>
    </nav>

    <!-- Conteúdo Principal -->
    <div class="container">
        <!-- Título -->
        <div class="row">
            <div class="col">
                <h1>Detalhamento do Projeto</h1>
                <p class="lead">Descrição geral e etapas do meu projeto de desenvolvimento de sistema.</p>
            </div>
        </div>

        <!-- Seção 1 - Descrição do Projeto -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4>Visão Geral</h4>
                    </div>
                    <div class="card-body">
                        <p>Este projeto envolve o desenvolvimento de um sistema para gerenciamento de produtos, com
                            integração de uma API backend e um sistema de busca no catálogo. A arquitetura do sistema
                            inclui o uso de tecnologias como TomCat 9, MySQL, e desenvolvimento de interfaces de
                            usuário para Web e App.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4>Objetivos</h4>
                    </div>
                    <div class="card-body">
                        <ul>
                            <li>Desenvolver APIs para cadastro e gerenciamento de produtos</li>
                            <li>Implementar um sistema de análise de dados</li>
                            <li>Realizar testes unitários e de integração</li>
                            <li>Configurar pipeline de CI/CD e deploy em produção</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- Seção 2 - Fluxograma do Projeto -->
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-header">
                        <h4>Fluxograma do Projeto</h4>
                    </div>
                    <div class="card-body">
                        <div class="mermaid">
                            graph TD
                                A1[Definir Escopo Detalhado] --> A2[Escolher Tecnologias Frontend]
                                A2 --> A3[Configuração do Ambiente de Desenvolvimento]
                                A3 --> A4[Criar Estrutura de Diretórios e Repositório Git]
                                
                                A4 --> B1[Configurar Servidor TomCat 9]
                                B1 --> B2[Desenvolver API para Cadastro de Lojistas]
                                B2 --> B3[Implementar Banco de Dados MySQL]
                                B3 --> B4[Desenvolver API para Gerenciamento de Produtos]
                                B4 --> B5[Implementar Sistema de Análise de Dados]
                                B5 --> B6[Desenvolver Módulo de Registro de Preços]
                                
                                A4 --> C1[Criar Interfaces de Usuário - Web e App]
                                C1 --> C2[Integração com API Backend]
                                C2 --> C3[Desenvolver Sistema de Busca no Catalogo]
                                
                                B4 --> D1[Identificar Fontes de Dados]
                                D1 --> D2[Tratamento ETL]
                                D2 --> D3[Integrar Dados ao Sistema]
                                
                                B6 --> E1[Testes Unitários e de Integração]
                                C3 --> E2[Testes de Interface de Usuário]
                                D3 --> E3[Testes de Performance]
                                
                                E1 --> E4[Testes de Integração e Validação]
                                E2 --> E4
                                E3 --> E4
                                
                                E4 --> F1[Configurar Pipeline de CI/CD]
                                F1 --> F2[Deploy em Ambiente de Produção]
                                F2 --> F3[Monitoramento e Logging]
                                
                                F3 --> I[Entrega Final]
                                
                                G1[Revisão de Literatura] --> G2[Escrever Introdução]
                                G2 --> G3[Descrever Metodologia]
                                G3 --> G4[Documentar Desenvolvimento]
                                G4 --> G5[Análise de Resultados]
                                G5 --> G6[Escrever Conclusão]
                                G6 --> G7[Revisão e Edição]
                                G7 --> G8[Formatação Final]
                                G8 --> G9[Revisão por Orientador]
                                
                                G9 --> H1[Roteirizar Apresentação]
                                H1 --> H2[Gravação e Edição]
                                H2 --> H3[Feedback e Ajustes]
                                
                                H3 --> I
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Seção 3 - Etapas do Projeto -->
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-header">
                        <h4>Etapas do Projeto</h4>
                    </div>
                    <div class="card-body">
                        <ul>
                            <li>Desenvolvimento de backend e integração com banco de dados</li>
                            <li>Criação de interfaces de usuário responsivas</li>
                            <li>Testes e validação de funcionalidades</li>
                            <li>Configuração de CI/CD para deploy automatizado</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Bootstrap JS and Popper.js -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.min.js"></script>
</body>

</html>
