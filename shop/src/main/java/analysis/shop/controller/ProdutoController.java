package analysis.shop.controller;

import java.io.IOException;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.annotation.*;
import analysis.shop.model.Produto;

/**
 * Servlet implementation class ProdutoController
 */
@WebServlet("/ProdutoController")
public class ProdutoController extends HttpServlet {
	private static final long serialVersionUID = 1L;

    
    public ProdutoController() {
        
    }

	
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String id = request.getParameter("id");
        if (id != null) {
            // Procura o produto pelo ID
            Produto produto = buscarProdutoPorId(id); // Método para buscar o produto
            request.setAttribute("produto", produto);
            request.getRequestDispatcher("/editarProduto.jsp").forward(request, response);
        } else {
            // Carrega a lista de produtos
            request.setAttribute("produtos", produtos);
            request.getRequestDispatcher("/produtos.jsp").forward(request, response);
        }
    }


	
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Criar novo produto ou atualizar existente
        String id = request.getParameter("id");
        String nome = request.getParameter("nome");
        String descricao = request.getParameter("descricao");
        String categoria = request.getParameter("categoria");
        double preco = Double.parseDouble(request.getParameter("preco"));
        String sku = request.getParameter("sku");
        int quantidadeEmEstoque = Integer.parseInt(request.getParameter("quantidadeEmEstoque"));

        if (id != null) {
            // Atualiza produto existente
            Produto produtoAtualizado = new Produto(id, nome, descricao, categoria, preco, sku, quantidadeEmEstoque);
            atualizarProduto(produtoAtualizado); // Método para atualizar o produto
        } else {
            // Adiciona novo produto
            Produto novoProduto = new Produto(id, nome, descricao, categoria, preco, sku, quantidadeEmEstoque);
            produtos.add(novoProduto); // Adiciona à lista
        }

        response.sendRedirect("produtos"); // Redireciona para a lista de produtos
    }


}
