package analysis.shop.controller;

import analysis.shop.model.Produto;
import analysis.shop.model.ProdutoDAO;

import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.*;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
//import javax.servlet.annotation.*;

//import javax.servlet.http.HttpSession;
//import controller.RequestDispatcher;


@WebServlet(name = "ProdutoController", urlPatterns = {"/ProdutoController"})
public class ProdutoController extends HttpServlet {
	private static final long serialVersionUID = 1L;

    
  	
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    	 String acao = (String) request.getParameter("acao");
    	 Produto produto = new Produto();
    	 ProdutoDAO produtoDAO = new ProdutoDAO();
    	 
         RequestDispatcher rd ;
          switch (acao) {
          case "Projeto":
        	  rd = request.getRequestDispatcher("/projeto.jsp");
              rd.forward(request, response);
              break;
          case "Adicionar":
        	  rd = request.getRequestDispatcher("/novoProduto.jsp");
              rd.forward(request, response);
              break;
          case "Dashboard":
        	  try {
                  ArrayList<Produto> listaProdutos = null;
				try {
					listaProdutos = produtoDAO.ListaDeProdutos();
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
                  request.setAttribute("msgOperacaoRealizada", "");
                  request.setAttribute("listaProdutos", listaProdutos);
                  rd = request.getRequestDispatcher("/produto.jsp");
                  rd.forward(request, response);

              } catch (IOException | ServletException ex) {
                  System.out.println(ex.getMessage());
                  throw new RuntimeException("Falha na query listar Produtos (Produto) ");
              }	
              break;
          case "Listar":
              try {
                  ArrayList<Produto> listaProdutos = null;
				try {
					listaProdutos = produtoDAO.ListaDeProdutos();
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
                  request.setAttribute("msgOperacaoRealizada", "");
                  request.setAttribute("listaProdutos", listaProdutos);
                  rd = request.getRequestDispatcher("/produtos.jsp");
                  rd.forward(request, response);

              } catch (IOException | ServletException ex) {
                  System.out.println(ex.getMessage());
                  throw new RuntimeException("Falha na query listar Produtos (Produto) ");
              }	
              break;
          case "Alterar":
        	  String idAlterar = request.getParameter("id");
              try {
                  produto = produtoDAO.getProduto(idAlterar); // Método que retorna o produto pelo ID
                  request.setAttribute("produto", produto); // Passa o produto para o formulário de edição
                  rd = request.getRequestDispatcher("/editarProduto.jsp"); // Página de edição
                  rd.forward(request, response);
              } catch (Exception e) {
                  e.printStackTrace();
                  throw new RuntimeException("Erro ao carregar produto para alteração.");
              }
              break;
        	  
          case "Excluir":
             /* try {
                  String id = request.getParameter("id");
                  produto = ProdutoDAO.getProduto(id);
                  produto.setId(id);
              } catch (Exception ex) {
                  System.out.println(ex.getMessage());
                  throw new RuntimeException("Falha em uma query para cadastro de usuario");
              }
              break;*/
        	  
        	  // Excluir o produto
              String idExcluir = request.getParameter("id");
              try {
                  produtoDAO.Excluir(idExcluir); // Chama o método para excluir
                  request.setAttribute("msgOperacaoRealizada", "Produto excluído com sucesso.");
              } catch (Exception e) {
                  request.setAttribute("msgOperacaoERRO", "Erro ao excluir o produto.");
                  e.printStackTrace();
              }
              response.sendRedirect("ProdutoController?acao=Listar"); // Redireciona para a lista de produtos
              break;
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
        ProdutoDAO produtoDAO = new ProdutoDAO();
        if (id != null && !id.isEmpty()) {
            // Atualiza produto existente
            //Produto produtoAtualizado = new Produto();
            //atualizarProduto(produtoAtualizado); // Método para atualizar o produto
        	Produto produto = new Produto();
        	produtoDAO = new ProdutoDAO();
            produto.setId(id); 
            produto.setNome(nome);
            produto.setDescricao(descricao); 
            produto.setCategoria(categoria);
            produto.setPreco(preco); 
            produto.setSku(sku); 
            produto.setQuantidadeEmEstoque(quantidadeEmEstoque);

            try {
                // Chama o método Alterar do ProdutoDAO
                produtoDAO.Alterar(produto);
                request.setAttribute("msgOperacaoRealizada", "Produto atualizado com sucesso");
                
            } catch (Exception e) {
                request.setAttribute("msgOperacaoERRO", "Erro ao atualizar o produto");
                e.printStackTrace();
            }
        	
        } else {
            // Adiciona novo produto
            Produto novoProduto = new Produto();
            //novoProduto.setId(id); 
            novoProduto.setNome(nome); 
            novoProduto.setDescricao(descricao); 
            novoProduto.setCategoria(categoria); 
            novoProduto.setPreco(preco); 
            novoProduto.setSku(sku); 
            novoProduto.setQuantidadeEmEstoque(quantidadeEmEstoque); 
            produtoDAO = new ProdutoDAO();
			try {
				produtoDAO.Inserir(novoProduto);
				request.setAttribute("msgOperacaoRealizada", "Inclusão realizada com sucesso");
			} catch (Exception e) {
				request.setAttribute("msgOperacaoERRO", "Inclusão não realizada");
				e.printStackTrace();
			} 
        }

        // Após modificar ou incluir, carrega a lista de produtos
        ArrayList<Produto> listaProdutos = produtoDAO.ListaDeProdutos();
        request.setAttribute("listaProdutos", listaProdutos);
        RequestDispatcher rd = request.getRequestDispatcher("/produtos.jsp");
        rd.forward(request, response);
    }


}
