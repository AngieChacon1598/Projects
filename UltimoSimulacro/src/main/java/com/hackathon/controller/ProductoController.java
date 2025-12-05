package com.hackathon.controller;

import com.hackathon.entity.Producto;
import com.hackathon.repository.ProductoRepository;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/productos")
@CrossOrigin(origins = "*")
public class ProductoController {
    
    private static final Logger logger = LoggerFactory.getLogger(ProductoController.class);
    
    @Autowired
    private ProductoRepository productoRepository;
    
    @GetMapping
    public ResponseEntity<List<Producto>> getAllProductos() {
        logger.info("=== OPERACIÓN CRUD: GET - Listar todos los productos ===");
        List<Producto> productos = productoRepository.findAll();
        logger.info("Productos encontrados: {}", productos.size());
        logger.debug("Lista de productos: {}", productos);
        return ResponseEntity.ok(productos);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Producto> getProductoById(@PathVariable Long id) {
        logger.info("=== OPERACIÓN CRUD: GET - Obtener producto por ID: {} ===", id);
        Optional<Producto> producto = productoRepository.findById(id);
        if (producto.isPresent()) {
            logger.info("Producto encontrado: ID={}, Nombre={}", id, producto.get().getNombre());
            return ResponseEntity.ok(producto.get());
        } else {
            logger.warn("Producto no encontrado con ID: {}", id);
            return ResponseEntity.notFound().build();
        }
    }
    
    @PostMapping
    public ResponseEntity<Producto> createProducto(@Valid @RequestBody Producto producto) {
        logger.info("=== OPERACIÓN CRUD: POST - Crear nuevo producto ===");
        logger.info("Datos del producto a crear - Nombre: {}, Descripción: {}, Precio: {}, Stock: {}", 
                producto.getNombre(), producto.getDescripcion(), producto.getPrecio(), producto.getStock());
        Producto nuevoProducto = productoRepository.save(producto);
        logger.info("Producto creado exitosamente - ID: {}, Nombre: {}", nuevoProducto.getId(), nuevoProducto.getNombre());
        return ResponseEntity.status(HttpStatus.CREATED).body(nuevoProducto);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Producto> updateProducto(@PathVariable Long id, 
                                                    @Valid @RequestBody Producto productoDetails) {
        logger.info("=== OPERACIÓN CRUD: PUT - Actualizar producto con ID: {} ===", id);
        logger.info("Datos a actualizar - Nombre: {}, Descripción: {}, Precio: {}, Stock: {}", 
                productoDetails.getNombre(), productoDetails.getDescripcion(), 
                productoDetails.getPrecio(), productoDetails.getStock());
        Optional<Producto> productoOptional = productoRepository.findById(id);
        
        if (productoOptional.isPresent()) {
            Producto producto = productoOptional.get();
            logger.debug("Producto actual antes de actualizar: {}", producto);
            producto.setNombre(productoDetails.getNombre());
            producto.setDescripcion(productoDetails.getDescripcion());
            producto.setPrecio(productoDetails.getPrecio());
            producto.setStock(productoDetails.getStock());
            
            Producto productoActualizado = productoRepository.save(producto);
            logger.info("Producto actualizado exitosamente - ID: {}, Nombre: {}", 
                    productoActualizado.getId(), productoActualizado.getNombre());
            return ResponseEntity.ok(productoActualizado);
        }
        
        logger.warn("Producto no encontrado para actualizar con ID: {}", id);
        return ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProducto(@PathVariable Long id) {
        logger.info("=== OPERACIÓN CRUD: DELETE - Eliminar producto con ID: {} ===", id);
        if (productoRepository.existsById(id)) {
            Optional<Producto> producto = productoRepository.findById(id);
            if (producto.isPresent()) {
                logger.info("Eliminando producto - ID: {}, Nombre: {}", id, producto.get().getNombre());
            }
            productoRepository.deleteById(id);
            logger.info("Producto eliminado exitosamente - ID: {}", id);
            return ResponseEntity.noContent().build();
        }
        
        logger.warn("Producto no encontrado para eliminar con ID: {}", id);
        return ResponseEntity.notFound().build();
    }
    
    @GetMapping("/buscar")
    public ResponseEntity<List<Producto>> buscarProductos(@RequestParam String nombre) {
        logger.info("=== OPERACIÓN CRUD: GET - Buscar productos por nombre: '{}' ===", nombre);
        List<Producto> productos = productoRepository.findByNombreContainingIgnoreCase(nombre);
        logger.info("Productos encontrados en búsqueda: {}", productos.size());
        logger.debug("Resultados de búsqueda: {}", productos);
        return ResponseEntity.ok(productos);
    }
}

