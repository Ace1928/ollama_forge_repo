/**
 * 🌀 Eidosian Enhancer - Intelligent Interactive Components
 * 
 * This script adds advanced interactive behaviors to Eidosian documentation,
 * following principles of Velocity as Intelligence and Flow Like a River.
 */

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    /**
     * 🧠 Contextual integrity: Functions are isolated and purposeful
     */

    // Enhance code blocks with language indicators
    function enhanceCodeBlocks() {
        document.querySelectorAll('div.highlight').forEach(block => {
            const pre = block.querySelector('pre');
            if (!pre) return;

            // Detect language from classes
            const classList = pre.className.split(' ');
            let lang = 'code';

            for (const cls of classList) {
                if (cls.startsWith('language-')) {
                    lang = cls.replace('language-', '');
                    break;
                }
            }

            // Set data attribute for CSS to use
            block.setAttribute('data-language', lang);

            // Add copy button if not already present
            if (!block.querySelector('.highlight-copy-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'highlight-copy-btn';
                copyBtn.textContent = 'Copy';
                copyBtn.setAttribute('aria-label', 'Copy code to clipboard');

                copyBtn.addEventListener('click', function () {
                    const code = pre.textContent;
                    navigator.clipboard.writeText(code).then(() => {
                        copyBtn.textContent = 'Copied!';
                        copyBtn.classList.add('copied');

                        setTimeout(() => {
                            copyBtn.textContent = 'Copy';
                            copyBtn.classList.remove('copied');
                        }, 2000);
                    });
                });

                block.appendChild(copyBtn);
            }
        });
    }

    // Create mobile-friendly collapsible sections
    function createCollapsibleSections() {
        if (window.innerWidth <= 768) {
            document.querySelectorAll('h2, h3').forEach(heading => {
                // Skip headings that are already in collapsible sections
                if (heading.closest('.mobile-toggle-section')) return;

                // Create collapsible wrapper
                const section = document.createElement('div');
                section.className = 'mobile-toggle-section';

                // Get all elements until the next heading of same or higher level
                const content = document.createElement('div');
                content.className = 'content';

                let sibling = heading.nextElementSibling;
                const elementsToMove = [];

                while (sibling &&
                    !(sibling.tagName === 'H2' ||
                        (heading.tagName === 'H3' && sibling.tagName === 'H3'))) {
                    elementsToMove.push(sibling);
                    sibling = sibling.nextElementSibling;
                }

                // Move elements to content div
                elementsToMove.forEach(el => {
                    content.appendChild(el);
                });

                // Create header from the heading
                const header = document.createElement('div');
                header.className = 'header';
                header.innerHTML = heading.innerHTML;

                // Replace heading with our collapsible section
                heading.parentNode.replaceChild(section, heading);
                section.appendChild(header);
                section.appendChild(content);

                // Add click handler
                header.addEventListener('click', () => {
                    section.classList.toggle('active');
                });
            });
        }
    }

    // Add table of contents highlight on scroll
    function setupTocHighlight() {
        const headings = Array.from(document.querySelectorAll('h1[id], h2[id], h3[id]'));
        const tocLinks = Array.from(document.querySelectorAll('.toc-tree a'));

        if (headings.length === 0 || tocLinks.length === 0) return;

        function highlightTocLink() {
            // Find the heading that's currently in view
            let currentHeading = null;

            for (const heading of headings) {
                const rect = heading.getBoundingClientRect();
                if (rect.top <= 100) {  // Adjust the offset as needed
                    currentHeading = heading;
                } else {
                    break;
                }
            }

            // Highlight the corresponding TOC link
            if (currentHeading) {
                const headingId = currentHeading.getAttribute('id');

                // Remove active class from all links
                tocLinks.forEach(link => {
                    link.classList.remove('active');
                });

                // Add active class to matching link
                const activeLink = tocLinks.find(link => {
                    return link.getAttribute('href') === `#${headingId}`;
                });

                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        }

        // Run initially and on scroll
        highlightTocLink();
        window.addEventListener('scroll', highlightTocLink, { passive: true });
    }

    // Initialize theme toggle functionality
    function setupThemeToggle() {
        const toggles = document.querySelectorAll('.theme-toggle');

        toggles.forEach(toggle => {
            toggle.addEventListener('click', function () {
                let theme = document.body.dataset.theme;

                if (theme === 'dark') {
                    document.body.dataset.theme = 'light';
                    localStorage.setItem('theme', 'light');
                } else if (theme === 'light') {
                    document.body.dataset.theme = 'auto';
                    localStorage.removeItem('theme');
                } else {
                    document.body.dataset.theme = 'dark';
                    localStorage.setItem('theme', 'dark');
                }
            });
        });
    }

    // Create FAQ components
    function setupFaqComponents() {
        document.querySelectorAll('.eidosian-faq').forEach(faq => {
            const question = faq.querySelector('.eidosian-faq-question');
            if (!question) return;

            question.addEventListener('click', () => {
                faq.classList.toggle('eidosian-faq-open');
            });

            // Add keyboard accessibility
            question.setAttribute('tabindex', '0');
            question.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    faq.classList.toggle('eidosian-faq-open');
                }
            });
        });
    }

    // Main initialization 
    function initialize() {
        enhanceCodeBlocks();
        setupThemeToggle();
        setupFaqComponents();
        setupTocHighlight();

        // Only create collapsible sections on small screens
        if (window.innerWidth <= 768) {
            createCollapsibleSections();
        }

        // Add data attribute support
        document.querySelectorAll('[data-eidosian-toggle]').forEach(el => {
            const target = document.querySelector(el.dataset.eidosianToggle);
            if (!target) return;

            el.addEventListener('click', () => {
                const expanded = target.classList.toggle('eidosian-expanded');
                el.setAttribute('aria-expanded', expanded ? 'true' : 'false');
            });
        });
    }

    // Run initialization
    initialize();

    // Handle window resize events
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            // Re-run mobile-specific functions
            if (window.innerWidth <= 768) {
                createCollapsibleSections();
            }
        }, 250);
    });
});
