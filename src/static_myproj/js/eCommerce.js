$(document).ready(function() {
    // blocks normal submission of form and creates an ajax request
    let productForm = $('.ajax-product-form')
    productForm.submit(function(event) {
      event.preventDefault();
      let thisForm=$(this)
      let action = thisForm.attr('action');
      let httpmethod = thisForm.attr('method');
      let formData = thisForm.serialize();
      console.log(action, httpmethod, formData)
      $.ajax({
        url: action,
        method: httpmethod,
        data: formData,
        success: function(data){
          console.log('success', data)
                 // if view successfully handles form then want to update original html to change between added to cart and remove
                 let addbutton = thisForm.find('.alternate-add-button')
                 if (data.added) {
                  addbutton.html('Item in cart <button type="submit" class="btn btn-link">Remove from Cart?</button>')
                } else {
                  addbutton.html('<button type="submit" class="btn btn-danger">Add to Cart?</button>')
                }
                let navbarCartCount = $('.navbar-cart-count')
                if (data.cartCount > 0) {
                  navbarCartCount.text(data.cartCount)
                } else {
                  navbarCartCount.text('')
                }
                let currentPath = window.location.href
                if (currentPath.indexOf('cart') != -1) {
                  console.log('in index')
                  refreshCart()
                }
        },
        error: function(errorData){
          console.log('error', errorData)
        }
      })
    })
    function refreshCart() {
      let cartTable = $(".ajax-refresh-cart-table")
      let cartbody = cartTable.find(".ajax-refresh-cart-body")
      let subtotal = cartbody.find('.ajax-cart-subtotal')
      let total = cartbody.find('.ajax-cart-total')
      let cartRow = cartbody.find(".ajax-cart-row")
      let currentUrl = window.location.href
      console.log('test')
      $.ajax({
        url: 'api/refresh_cart/',
        method: 'GET',
        data: {},
        success: function(data) {
          console.log(data)
          if (data.products.length < 1) {
            window.location.href = currentUrl
          } else {
            let cartProductRemoveForm = $(".cart-product-remove-form")
            // cartProductRemoveForm.css('display', 'block')
            cartRow.html('')
            let counter = data.products.length
            $.each(data.products, function(index, value){
              let newCartProductRemoveForm = cartProductRemoveForm.clone().css('display', 'block')
              newCartProductRemoveForm.find(".api-cart-product-id").val(value.id)
              console.log(newCartProductRemoveForm.find(".api-cart-product-id").val())
              cartbody.prepend('<tr class="ajax-cart-row"><th scope="row">' + counter + '</th><td class="px-5" ><a href="' + value.url + '">' + value.name + ' ' + newCartProductRemoveForm.html() +'<td>' + value.price + '</td>')
              counter--
            })
            subtotal.text(data.subtotal)
            total.text(data.total)
          }
        },
        error: function(errorData) {
          console.log(errorData)
        }
      })
    }
    

    // Autosearch
    let searchForm = $(".search-form")
    let searchInput = searchForm.find("[name='q']")
    // results in anything inside search form that has attribute name of q
    let timer;
    let interval = 500
    let searchBtn = searchForm.find('[type="submit"]')

    searchInput.keyup(function(event) {
      clearTimeout(timer)
      timer = setTimeout(search, interval)
    })
    function search(){
      searchingVisual()
      let query = searchInput.val()
      setTimeout(function(){
        window.location.href = "search/?q="+query
      }, 1000) 
    }
    // add a loading button as a visual for searching
    function searchingVisual(){
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")
    }

    // contact form ajax
    let contactForm = $(".contact-form")
    contactForm.submit(function(event) {
      event.preventDefault()
      console.log('test')
      let thisForm = $(this)
      let contactMethod = contactForm.attr("method")
      let contactEndPoint = contactForm.attr("action")
      let contactData = contactForm.serialize()
      console.log(contactData)
      $.ajax({
        method: contactMethod,
        url: contactEndPoint,
        data: contactData,
        success: function(data) {
          thisForm[0].reset()
          $.alert({
            title: "Success!",
            content: data.message,
            theme: "modern",})
        },
        error: function(error) {
          let jsonErrorData = error.responseJSON
          let msg = ''

          $.each(jsonErrorData, function(key, value){
            msg += key + ": " + value[0].message + "<br>"
          })
          $.alert({
            title: "Alert",
            content: msg, 
            theme: "modern",})
        },
      })
    })
  })