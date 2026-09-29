package com.example.productinventory.repository;
import com.example.productinventory.model.Product; import org.springframework.data.jpa.repository.JpaRepository;
public interface ProductRepository extends JpaRepository<Product,Long> {}