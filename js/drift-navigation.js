/**
 * Drift Navigation Script
 * Provides navigation based on drift/journey order instead of traveling salesman
 */

(function() {
    'use strict';
    
    // Get Pacific West Coast Drift order (North to South)
    function getPacificWestCoastDriftOrder() {
        if (!window.PARTNERS_DATA) return [];
        
        const westCoastStates = ['Washington', 'Oregon', 'California', 'Arizona'];
        const filtered = {};
        
        for (const slug in window.PARTNERS_DATA) {
            const partner = window.PARTNERS_DATA[slug];
            const location = partner.location.toLowerCase();
            const isWestCoast = westCoastStates.some(state => 
                location.includes(state.toLowerCase())
            );
            if (isWestCoast) {
                filtered[slug] = partner;
            }
        }
        
        // Sort North to South (latitude descending)
        const slugs = Object.keys(filtered);
        return slugs.sort((a, b) => filtered[b].lat - filtered[a].lat);
    }
    
    // Get Brazilian Drift order (South to North: Founderhaus, then farms)
    function getBrazilianDriftOrder() {
        const order = ['founderhaus']; // Start with Founderhaus
        
        // Add farms in South to North order (latitude ascending)
        if (window.FARMS_DATA) {
            const brazilianFarms = {};
            for (const slug in window.FARMS_DATA) {
                const farm = window.FARMS_DATA[slug];
                if (farm.location.includes('Brazil')) {
                    brazilianFarms[slug] = farm;
                }
            }
            const farmSlugs = Object.keys(brazilianFarms);
            farmSlugs.sort((a, b) => brazilianFarms[a].lat - brazilianFarms[b].lat); // South to North
            order.push(...farmSlugs);
        }
        
        return order;
    }
    
    // Get neighbors in drift order
    function getDriftNeighbors(currentSlug, isPartner) {
        let order = [];
        let journeyUrl = '';
        
        if (isPartner) {
            // Check if partner is in Pacific West Coast drift
            const pacificOrder = getPacificWestCoastDriftOrder();
            if (pacificOrder.includes(currentSlug)) {
                order = pacificOrder;
                journeyUrl = '../../cacao-journeys/pacific-west-coast-path/index.html';
            } else if (currentSlug === 'founderhaus') {
                // Founderhaus is in Brazilian drift
                order = getBrazilianDriftOrder();
                journeyUrl = '../../cacao-journeys/brazilian-path/index.html';
            } else {
                // Partner not in any drift - return null
                return { previous: null, next: null, journeyUrl: null };
            }
        } else {
            // Farm - check if in Brazilian drift
            order = getBrazilianDriftOrder();
            if (order.includes(currentSlug)) {
                journeyUrl = '../../cacao-journeys/brazilian-path/index.html';
            } else {
                return { previous: null, next: null, journeyUrl: null };
            }
        }
        
        const currentIndex = order.indexOf(currentSlug);
        if (currentIndex === -1) {
            return { previous: null, next: null, journeyUrl: null };
        }
        
        const prevSlug = currentIndex > 0 ? order[currentIndex - 1] : null;
        const nextSlug = currentIndex < order.length - 1 ? order[currentIndex + 1] : null;
        
        let previous = null;
        let next = null;
        
        if (prevSlug) {
            if (prevSlug === 'founderhaus') {
                previous = window.PARTNERS_DATA ? window.PARTNERS_DATA[prevSlug] : null;
            } else if (isPartner) {
                previous = window.PARTNERS_DATA[prevSlug];
            } else {
                previous = window.FARMS_DATA ? window.FARMS_DATA[prevSlug] : null;
            }
        }
        
        if (nextSlug) {
            if (nextSlug === 'founderhaus') {
                next = window.PARTNERS_DATA ? window.PARTNERS_DATA[nextSlug] : null;
            } else if (isPartner) {
                next = window.PARTNERS_DATA[nextSlug];
            } else {
                next = window.FARMS_DATA ? window.FARMS_DATA[nextSlug] : null;
            }
        }
        
        return { previous, next, journeyUrl };
    }
    
    // Expose to window
    window.getDriftNeighbors = getDriftNeighbors;
    window.getPacificWestCoastDriftOrder = getPacificWestCoastDriftOrder;
    window.getBrazilianDriftOrder = getBrazilianDriftOrder;
})();

