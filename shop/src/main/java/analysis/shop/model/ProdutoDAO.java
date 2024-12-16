package analysis.shop.model;

import java.math.BigDecimal;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import analysis.shop.model.Produto;
import analysis.shop.model.Conexao;

public class ProdutoDAO {
	 public void Inserir(Produto produto) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	        	PreparedStatement sql = conexao.getConexao().prepareStatement(
	        		    "INSERT INTO produto (nome, descricao, categoria, preco, sku, quantidadeEmEstoque, ativo, avaliacao, numeroDeVendas) "
	        		    + "VALUES (?, ?, ?, ?, ?, ?, 1, 0.00, 0)");
	            //sql.setString(1, produto.getId());
	            sql.setString(1, produto.getNome());
	            sql.setString(2, produto.getDescricao());
	            sql.setString(3, produto.getCategoria());
	            sql.setBigDecimal(4, BigDecimal.valueOf(produto.getPreco()));
	            sql.setString(5, produto.getSku());
	            sql.setInt(6, produto.getQuantidadeEmEstoque());
	            sql.executeUpdate();

	        } catch (SQLException e) {
	            throw new RuntimeException();
	        } finally {
	            conexao.closeConexao();
	        }
	    }

	    public Produto getProduto(String id) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	        	Produto produto = new Produto();
	            PreparedStatement sql = conexao.getConexao().prepareStatement("SELECT * FROM produto WHERE ID = ? ");
	            sql.setString(1, id);
	            ResultSet resultado = sql.executeQuery();
	            if (resultado != null) {
	                while (resultado.next()) {
	                	produto.setId(resultado.getString("id"));
	                	produto.setNome(resultado.getString("nome"));
	                	produto.setDescricao(resultado.getString("descricao"));
	                	produto.setCategoria(resultado.getString("categoria"));
	                	produto.setPreco(resultado.getDouble("preco"));
	                	produto.setSku(resultado.getString("sku"));
	                	produto.setQuantidadeEmEstoque(resultado.getInt("quantidadeEmEstoque"));
	                }
	            }
	            return produto;

	        } catch (SQLException e) {
	            throw new RuntimeException("Query de select (get) incorreta");
	        } finally {
	            conexao.closeConexao();
	        }
	    }
	    
	    /* 

	    public void Alterar(Usuario Usuario) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	            PreparedStatement sql = conexao.getConexao().prepareStatement("UPDATE usuarios SET nome = ?, cpf = ?, endereco = ?, senha = ?  WHERE ID = ? ");
	            sql.setString(1, Usuario.getNome());
	            sql.setString(2, Usuario.getCpf());
	            sql.setString(3, Usuario.getEndereco());
	            sql.setString(4, Usuario.getSenha());
	            sql.setInt(5, Usuario.getId());
	            sql.executeUpdate();

	        } catch (SQLException e) {
	            throw new RuntimeException("Query de update (alterar) incorreta");
	        } finally {
	            conexao.closeConexao();
	        }
	    }

	    public void Excluir(Usuario Usuario) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	            PreparedStatement sql = conexao.getConexao().prepareStatement("DELETE FROM usuarios WHERE ID = ? ");
	            sql.setInt(1, Usuario.getId());
	            sql.executeUpdate();

	        } catch (SQLException e) {
	            throw new RuntimeException("Query de delete (excluir) incorreta");
	        } finally {
	            conexao.closeConexao();
	        }
	    }    */
	    
	    
	    public void Alterar(Produto produto) throws Exception {
        Conexao conexao = new Conexao();
        try {
            // Query SQL para atualizar os dados do produto
            PreparedStatement sql = conexao.getConexao().prepareStatement(
                "UPDATE produto SET nome = ?, descricao = ?, categoria = ?, preco = ?, sku = ?, quantidadeEmEstoque = ? WHERE id = ?"
            );
            // Atribui os parâmetros ao PreparedStatement
            sql.setString(1, produto.getNome());
            sql.setString(2, produto.getDescricao());
            sql.setString(3, produto.getCategoria());
            sql.setDouble(4, produto.getPreco());
            sql.setString(5, produto.getSku());
            sql.setInt(6, produto.getQuantidadeEmEstoque());
            sql.setString(7, produto.getId()); // Definindo o ID para localizar o produto a ser alterado

            // Executa a atualização
            sql.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Query de update (alterar) incorreta: " + e.getMessage());
        } finally {
            conexao.closeConexao();
        }
    }
	    
	    public void Excluir(String id) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	            // Query SQL para excluir o produto
	            PreparedStatement sql = conexao.getConexao().prepareStatement("DELETE FROM produto WHERE id = ?");
	            // Define o parâmetro (id) para identificar o produto a ser excluído
	            sql.setString(1, id);

	            // Executa a exclusão
	            sql.executeUpdate();
	        } catch (SQLException e) {
	            throw new RuntimeException("Query de delete (excluir) incorreta: " + e.getMessage());
	        } finally {
	            conexao.closeConexao();
	        }
	    }    
	    

	    public  ArrayList<Produto> ListaDeProdutos() {
	        ArrayList<Produto> meusProdutos = new ArrayList<Produto>();
	        Conexao conexao = new Conexao();
	        try {
	            String selectSQL = "SELECT * FROM produto order by nome";
	            PreparedStatement preparedStatement;
	            preparedStatement = conexao.getConexao().prepareStatement(selectSQL);
	            ResultSet resultado = preparedStatement.executeQuery();
	            if (resultado != null) {
	                while (resultado.next()) {
	                	Produto produto = new Produto();
	                	produto.setId(resultado.getString("id"));
	                	produto.setNome(resultado.getString("nome"));
	                	produto.setDescricao(resultado.getString("descricao"));
	                	produto.setCategoria(resultado.getString("categoria"));
	                	produto.setPreco(resultado.getDouble("preco"));
	                	produto.setSku(resultado.getString("sku"));
	                	produto.setQuantidadeEmEstoque(resultado.getInt("quantidadeEmEstoque"));
	                	meusProdutos.add(produto);
	                }
	            }
	        } catch (SQLException e) {
	            throw new RuntimeException("Query de select (ListaDeUsuarios) incorreta");
	        } finally {
	            conexao.closeConexao();
	        }
	        return meusProdutos;
	    }
/*
	    public Usuario Logar(Usuario usuario) throws Exception {
	        Conexao conexao = new Conexao();
	        try {
	            PreparedStatement sql = conexao.getConexao().prepareStatement("SELECT * FROM usuarios WHERE cpf=? and senha =? LIMIT 1");
	            sql.setString(1, usuario.getCpf());
	            sql.setString(2, usuario.getSenha());
	            ResultSet resultado = sql.executeQuery();
	            Usuario usuarioObtido = new Usuario();
	            if (resultado != null) {
	                while (resultado.next()) {
	                    usuarioObtido.setId(Integer.parseInt(resultado.getString("ID")));
	                    usuarioObtido.setNome(resultado.getString("NOME"));
	                    usuarioObtido.setCpf(resultado.getString("CPF"));
	                    usuarioObtido.setEndereco(resultado.getString("ENDERECO"));
	                    usuarioObtido.setSenha(resultado.getString("SENHA"));
	                }
	            }
	            return usuarioObtido;

	        } catch (SQLException e) {
	            System.out.println(e.getMessage());
	            throw new RuntimeException("Query de select (get) incorreta");
	        } finally {
	            conexao.closeConexao();
	        }
	    }
	    */
}
