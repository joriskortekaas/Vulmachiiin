CREATE TABLE products (id INT PRIMARY KEY,
                       name VARCHAR(64) NOT NULL,
                       amount_in_stock INT NOT NULL DEFAULT 0,
                       cartridge_type INT NOT NULL DEFAULT 1,
                       amount_per_cartridge INT NOT NULL DEFAULT 0);

CREATE TABLE shelves (id INT PRIMARY KEY,
                      size_horizontal INT NOT NULL DEFAULT 1,
                      size_vertical INT NOT NULL DEFAULT 3);

CREATE TABLE productsinshelve (product_id INT,
                               shelf_id INT,
                               x_coordinate INT NOT NULL,
                               y_coordinate INT NOT NULL,
                               amount_in_cartridge INT NOT NULL,
                               CONSTRAINT PK_productsinshelve PRIMARY KEY (product_id, shelf_id),
                               FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                               FOREIGN KEY (shelf_id) REFERENCES shelves(id) ON DELETE CASCADE);

CREATE TABLE nodes (id INT PRIMARY KEY,
                    shelve_id INT,
                    FOREIGN KEY (shelve_id) REFERENCES shelves (id));

CREATE TABLE edges (edge_id INT PRIMARY KEY,
                    node_one_id INT,
                    node_two_id INT,
                    weight INT NOT NULL,
                    FOREIGN KEY (node_one_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY (node_two_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    CONSTRAINT unique_nodes UNIQUE (node_one_id, node_two_id));

CREATE TABLE edgeconnections (edge_one_id INT,
                              direction INT NOT NULL,
                              edge_two_id INT,
                              CONSTRAINT PK_edgeconnections PRIMARY KEY (edge_one_id, edge_two_id),
                              FOREIGN KEY (edge_one_id) REFERENCES edges(edge_id) ON DELETE CASCADE,
                              FOREIGN KEY (edge_two_id) REFERENCES edges(edge_id) ON DELETE CASCADE,
                              CONSTRAINT unique_edges UNIQUE (edge_one_id, edge_two_id));