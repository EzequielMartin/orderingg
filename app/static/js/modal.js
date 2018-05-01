const Modal = (function () {

    /**
     * Abre el modal
     **/
    function open($modal,tipo,producto) {
        const editTitle = document.getElementById('edit-title');
        const saveTitle = document.getElementById('save-title');
        const editButton = document.getElementById('edit-button');
        const saveButton = document.getElementById('save-button');
	const nombreproducto = document.getElementById('name-product');



	    if( tipo === 'agregar'){

		editButton.classList.add('is-hidden');
		editTitle.classList.add('is-hidden');
		saveButton.classList.remove('is-hidden');
		saveTitle.classList.remove('is-hidden');
		document.getElementById('select-prod').disabled=false;    
		
		$modal.classList.add('is-active');    




	    }else if( tipo === 'editar') {

		saveButton.classList.add('is-hidden');
		saveTitle.classList.add('is-hidden');
		editTitle.classList.remove('is-hidden');
		editButton.classList.remove('is-hidden');
		document.getElementById('select-prod').disabled=true;    
		document.getElementById('quantity').value=producto.quantity;
		$modal.classList.add('is-active');    
		    



	  API.getOrderProduct(1,producto.id)
	
	    .then(function (ProductoElegido){        
          document.getElementById('quantity').value=ProductoElegido["quantity"];
          var nombreProducto;
          nombreProducto = ProductoElegido["name"];
          var opcion;
          switch(nombreProducto) {
          case "Silla":
          opcion=1;
          break;
          case "Mesa":
          opcion=2;
          break;
          case "Vaso":
          opcion=3;
          break;
          case "Individual":
          opcion=4;
          break;}
           document.getElementById("select-prod").value=opcion;
          });





	    }


      







    }

    /**
     * Cierra el modal
     **/
    function close($modal) {
        $modal.classList.remove('is-active');
    }

    /**
     * Inicializa el modal de agregar producto
     **/
    function init(config) {
        const $modal = document.querySelector(config.el);

        // Inicializamos el select de productos
        Select.init({
            el: '#select',
            data: config.products,
            onSelect: config.onProductSelect
        });

        // Nos ponemos a escuchar cambios en el input de cantidad
        $modal.querySelector('#quantity')
            .addEventListener('input', function () {
                config.onChangeQunatity(this.value)
            });

        $modal.querySelector('#save-button')
            .addEventListener('click', config.onAddProduct);

	 $modal.querySelector('#edit-button')
              .addEventListener('click', config.onEditProduct);
	    

        return {
            close: close.bind(null, $modal),
            open: open.bind(null, $modal)
        }
    }

    return {
        init
    }
})();

