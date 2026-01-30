class MysuptechFooter extends HTMLElement {
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
                
                footer {
                    background: #0f172a;
                    color: #cbd5e1;
                    padding: 3rem 1.5rem 1.5rem;
                }
                
                .footer-container {
                    max-width: 1280px;
                    margin: 0 auto;
                }
                
                .footer-grid {
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 2rem;
                    margin-bottom: 2rem;
                }
                
                @media (min-width: 768px) {
                    .footer-grid {
                        grid-template-columns: 2fr 1fr 1fr 1fr;
                    }
                }
                
                .brand-section h3 {
                    color: white;
                    font-size: 1.25rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .brand-section p {
                    font-size: 0.875rem;
                    line-height: 1.6;
                    margin-bottom: 1rem;
                    color: #94a3b8;
                }
                
                .social-links {
                    display: flex;
                    gap: 1rem;
                }
                
                .social-links a {
                    color: #94a3b8;
                    transition: color 0.2s;
                }
                
                .social-links a:hover {
                    color: white;
                }
                
                .footer-column h4 {
                    color: white;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    font-size: 0.875rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                
                .footer-column ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                
                .footer-column li {
                    margin-bottom: 0.5rem;
                }
                
                .footer-column a {
                    color: #94a3b8;
                    text-decoration: none;
                    font-size: 0.875rem;
                    transition: color 0.2s;
                }
                
                .footer-column a:hover {
                    color: white;
                }
                
                .footer-bottom {
                    border-top: 1px solid #1e293b;
                    padding-top: 1.5rem;
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                    align-items: center;
                    text-align: center;
                    font-size: 0.875rem;
                    color: #64748b;
                }
                
                @media (min-width: 768px) {
                    .footer-bottom {
                        flex-direction: row;
                        justify-content: space-between;
                    }
                }
                
                .badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.25rem;
                    background: rgba(16, 185, 129, 0.1);
                    color: #10b981;
                    padding: 0.25rem 0.75rem;
                    border-radius: 9999px;
                    font-size: 0.75rem;
                    font-weight: 600;
                }
            </style>
            
            <footer>
                <div class="footer-container">
                    <div class="footer-grid">
                        <div class="brand-section">
                            <h3>
                                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="border-radius: 4px;">
                                    <rect width="32" height="32" rx="8" fill="#0ea5e9"/>
                                    <path d="M8 16L14 22L24 10" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                MySuptech
                            </h3>
                            <p>Plateforme de gestion pédagogique nouvelle génération pour ISI SUPTECH. Digitalisez votre établissement, simplifiez le suivi des cours et améliorez la communication entre administration et corps professoral.</p>
                            <div class="social-links">
                                <a href="#" aria-label="Twitter">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>
                                </a>
                                <a href="#" aria-label="LinkedIn">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
                                </a>
                                <a href="#" aria-label="GitHub">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
                                </a>
                            </div>
                        </div>
                        
                        <div class="footer-column">
                            <h4>Produit</h4>
                            <ul>
                                <li><a href="#features">Fonctionnalités</a></li>
                                <li><a href="#demo">Application Mobile</a></li>
                                <li><a href="#">Administration</a></li>
                                <li><a href="#">API Documentation</a></li>
                            </ul>
                        </div>
                        
                        <div class="footer-column">
                            <h4>Ressources</h4>
                            <ul>
                                <li><a href="#">Guide Utilisateur</a></li>
                                <li><a href="#">FAQ</a></li>
                                <li><a href="#">Support Technique</a></li>
                                <li><a href="#">Blog Pédagogique</a></li>
                            </ul>
                        </div>
                        
                        <div class="footer-column">
                            <h4>Légal</h4>
                            <ul>
                                <li><a href="#">Confidentialité</a></li>
                                <li><a href="#">Conditions d'utilisation</a></li>
                                <li><a href="#">RGPD</a></li>
                                <li><a href="#">Contact</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer-bottom">
                        <div>© 2026 MySuptech - ISI SUPTECH. Tous droits réservés.</div>
                    </div>
                </div>
            </footer>
        `;
    }
}

customElements.define('mysuptech-footer', MysuptechFooter);