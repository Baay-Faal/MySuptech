class MysuptechNavbar extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                }
                
                nav {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    z-index: 50;
                    transition: all 0.3s ease;
                }
                
                .nav-container {
                    max-width: 1280px;
                    margin: 0 auto;
                    padding: 1rem 1.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .logo {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-weight: 700;
                    font-size: 1.25rem;
                    color: white;
                    text-decoration: none;
                }
                
                .logo span {
                    background: linear-gradient(135deg, #10b981 0%, #0ea5e9 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                
                .nav-links {
                    display: none;
                    align-items: center;
                    gap: 2rem;
                }
                
                @media (min-width: 768px) {
                    .nav-links {
                        display: flex;
                    }
                }
                
                .nav-links a {
                    color: #cbd5e1;
                    text-decoration: none;
                    font-size: 0.875rem;
                    font-weight: 500;
                    transition: color 0.2s;
                }
                
                .nav-links a:hover {
                    color: white;
                }
                
                .cta-button {
                    background: #10b981;
                    color: white;
                    padding: 0.5rem 1.25rem;
                    border-radius: 0.5rem;
                    font-weight: 600;
                    font-size: 0.875rem;
                    text-decoration: none;
                    transition: all 0.2s;
                    border: none;
                    cursor: pointer;
                }
                
                .cta-button:hover {
                    background: #059669;
                    transform: translateY(-1px);
                }
                
                .mobile-menu-btn {
                    display: flex;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    padding: 0.5rem;
                }
                
                @media (min-width: 768px) {
                    .mobile-menu-btn {
                        display: none;
                    }
                }
                
                .mobile-menu {
                    display: none;
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: rgba(15, 23, 42, 0.98);
                    backdrop-filter: blur(10px);
                    padding: 1rem;
                    border-top: 1px solid rgba(255,255,255,0.1);
                }
                
                .mobile-menu.active {
                    display: block;
                }
                
                .mobile-menu a {
                    display: block;
                    color: #cbd5e1;
                    text-decoration: none;
                    padding: 0.75rem 1rem;
                    border-radius: 0.5rem;
                    transition: all 0.2s;
                }
                
                .mobile-menu a:hover {
                    background: rgba(255,255,255,0.1);
                    color: white;
                }
                
                .scrolled {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                }
                
                .scrolled .logo {
                    color: #0f172a;
                }
                
                .scrolled .nav-links a {
                    color: #475569;
                }
                
                .scrolled .nav-links a:hover {
                    color: #0f172a;
                }
                
                .scrolled .mobile-menu-btn {
                    color: #0f172a;
                }
            </style>
            
            <nav id="navbar">
                <div class="nav-container">
                    <a href="#" class="logo">
                        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect width="32" height="32" rx="8" fill="#0ea5e9"/>
                            <path d="M8 16L14 22L24 10" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>MySuptech</span>
                    </a>
                    <div class="nav-links">
                        <a href="index.html#features">Fonctionnalités</a>
                        <a href="index.html#demo">Interface Mobile</a>
                        <a href="index.html#live">Supervision</a>
                        <a href="{{ url_for('login') }}" class="cta-button">Se connecter</a>
</div>
<button class="mobile-menu-btn" id="mobile-toggle">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="3" y1="12" x2="21" y2="12"></line>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <line x1="3" y1="18" x2="21" y2="18"></line>
                        </svg>
                    </button>
                </div>
                <div class="mobile-menu" id="mobile-menu">
                    <a href="index.html#features">Fonctionnalités</a>
                    <a href="index.html#demo">Interface Mobile</a>
                    <a href="index.html#live">Supervision Live</a>
                    <a href="connexion.html" style="color: #10b981; font-weight: 600;">Se connecter →</a>
</div>
</nav>
        `;

        this.initScrollEffect();
        this.initMobileMenu();
    }

    initScrollEffect() {
        const nav = this.shadowRoot.getElementById('navbar');

        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    initMobileMenu() {
        const toggle = this.shadowRoot.getElementById('mobile-toggle');
        const menu = this.shadowRoot.getElementById('mobile-menu');

        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
        });

        // Close menu when clicking a link
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('active');
            });
        });
    }
}

customElements.define('mysuptech-navbar', MysuptechNavbar);