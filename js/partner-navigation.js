/**
 * Partner Navigation Script
 * Adds next/previous navigation based on drift/journey order
 */
(function() {
    'use strict';
    
    // Wait for partners data and drift navigation to load
    function initPartnerNavigation() {
        if (!window.PARTNERS_DATA || !window.getDriftNeighbors) {
            setTimeout(initPartnerNavigation, 100);
            return;
        }
        
        // Get current partner slug from URL
        const currentPath = window.location.pathname;
        const slugMatch = currentPath.match(/partners\/([^\/]+)\//);
        if (!slugMatch) return;
        
        const currentSlug = slugMatch[1];
        const result = window.getDriftNeighbors(currentSlug, true);
        
        if (!result || (!result.previous && !result.next)) return;
        
        const navContainer = document.getElementById('partner-navigation');
        if (!navContainer) return;
        
        let navHTML = '';
        
        // Previous partner
        if (result.previous) {
            const prevUrl = result.previous.slug === 'founderhaus' 
                ? '../founderhaus/index.html'
                : '../' + result.previous.slug + '/index.html';
            navHTML += '<a href="' + prevUrl + '" class="partner-nav-link previous">';
            navHTML += '<span class="partner-nav-label">← Previous</span>';
            navHTML += '<span class="partner-nav-name">' + result.previous.name + '</span>';
            navHTML += '</a>';
        } else {
            navHTML += '<div class="partner-nav-link previous disabled">';
            navHTML += '<span class="partner-nav-label">← Previous</span>';
            navHTML += '<span class="partner-nav-name">—</span>';
            navHTML += '</div>';
        }
        
        // Next partner
        if (result.next) {
            const nextUrl = result.next.slug === 'founderhaus'
                ? '../founderhaus/index.html'
                : '../' + result.next.slug + '/index.html';
            navHTML += '<a href="' + nextUrl + '" class="partner-nav-link next">';
            navHTML += '<span class="partner-nav-label">Next →</span>';
            navHTML += '<span class="partner-nav-name">' + result.next.name + '</span>';
            navHTML += '</a>';
        } else {
            navHTML += '<div class="partner-nav-link next disabled">';
            navHTML += '<span class="partner-nav-label">Next →</span>';
            navHTML += '<span class="partner-nav-name">—</span>';
            navHTML += '</div>';
        }
        
        navContainer.innerHTML = navHTML;
        
        // Update back link if journey URL is available
        if (result.journeyUrl) {
            const backLink = document.querySelector('.back-link');
            if (backLink) {
                backLink.href = result.journeyUrl;
                backLink.textContent = 'Back to Journey';
            }
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPartnerNavigation);
    } else {
        initPartnerNavigation();
    }
})();

