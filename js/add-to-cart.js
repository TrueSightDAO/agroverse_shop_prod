/**
 * Add to Cart Button Handler
 * Handles "Add to Cart" button clicks on product pages
 */

(function() {
  'use strict';

  // Prevent multiple initializations
  if (window.addToCartInitialized) {
    return;
  }
  window.addToCartInitialized = true;

  /**
   * Handle add to cart button click
   */
  function handleAddToCart(event) {
    event.preventDefault();
    event.stopPropagation(); // Prevent event from bubbling up

    const button = event.target.closest('.add-to-cart-btn');
    if (!button) return;

    // Prevent double-firing by checking if already processing
    if (button.dataset.processing === 'true') {
      return;
    }
    button.dataset.processing = 'true';

    // Get product data from data attributes
    const productId = button.dataset.productId;
    
    // Try to get full product data from window.PRODUCTS first (includes weight)
    let product;
    if (window.PRODUCTS && window.PRODUCTS[productId]) {
      product = Object.assign({}, window.PRODUCTS[productId], {
        quantity: 1
      });
    } else {
      // Fallback to data attributes if product not in PRODUCTS
      product = {
        productId: productId,
        name: button.dataset.productName,
        price: parseFloat(button.dataset.productPrice),
        image: button.dataset.productImage,
        stripePriceId: button.dataset.stripePriceId || '',
        weight: parseFloat(button.dataset.productWeight) || 0,
        quantity: 1
      };
    }

    // Validate product data
    if (!product.productId || !product.name || !product.price) {
      console.error('Invalid product data:', product);
      button.dataset.processing = 'false';
      return;
    }

    // Add to cart
    const success = window.Cart.add(product);

    // Reset processing flag after a short delay
    setTimeout(() => {
      button.dataset.processing = 'false';
    }, 500);

    // Cart badge will update automatically via cart event listeners
    // No toast notification - cleaner UX
  }

  /**
   * Initialize add to cart buttons
   */
  function initAddToCart() {
    // Use event delegation - single listener on document
    // This handles both existing and dynamically added buttons
    // Only add listener once (check if already added)
    if (!window.addToCartListenerAdded) {
      document.addEventListener('click', function(event) {
        if (event.target.closest('.add-to-cart-btn')) {
          handleAddToCart(event);
        }
      }, true); // Use capture phase to catch early
      window.addToCartListenerAdded = true;
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAddToCart);
  } else {
    initAddToCart();
  }

})();

