<template> 
  <div class="newsletter-section">
    <div class="newsletter-content">
      <p class="newsletter-title">Want to stay in touch? Sign up to receive news and updates from the Jirani Merchants team.</p>
      <div class="newsletter-form">
        <input type="email" placeholder="@gmail |  @proton.me | @tutamail.com"
         class="newsletter-input-field" />
        <button class="newsletter-signup-btn">SIGN UP</button>
      </div>
      <p class="newsletter-privacy">We respect your privacy.</p>
    </div>
  </div>
  <div class="footer-spacer" aria-hidden="true"></div>
  <footer :class="['business-footer', { 'footer-visible': isFooterVisible }]">
    <div class="footer-bottom-content">
      <ul class="footer-links-row">
        <div class="footer-links-left">
          <li><router-link to="/terms-of-use">Terms of Use</router-link></li>
          <li><router-link to="/privacy-policy">Privacy Policy</router-link></li>
        </div>
        <span class="footer-logo">
          <img src="../assets/JMerchant-Logo.png" alt="JMerchant-Logo">
        </span>
        <div class="footer-links-right">
          <li><router-link to="/cookie-policy">Cookie Policy</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
        </div>
      </ul>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      isFooterVisible: false,
    };
  },
  mounted() {
    window.addEventListener('scroll', this.checkScrollPosition);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.checkScrollPosition);
  },
  methods: {
    checkScrollPosition() {
      const scrollPosition = window.scrollY + window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      const distanceFromBottom = Math.max(0, documentHeight - scrollPosition);
      this.isFooterVisible = distanceFromBottom <= 4; // small threshold to avoid flicker
    },
  },
};
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Jersey+10&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

/* Use page palette and fonts */
  :root {
  --text-color: #191919;
  --extra-color: #f15025;
  --paragraph-color: #191919;
  --background-color: #fcfffc;
  /* semi-transparent version for the glass effect */
  --navbar-bg: rgba(252, 255, 252, 0.9); 
  }

  .newsletter-section {
    background: var(--paragraph-color);
    color: var(--background-color);
    padding: 60px 0 30px 0;
    text-align: center;
    margin: 7rem 0;
    font-family: "Montserrat", sans-serif;
  }

  .newsletter-title {
    font-family: "Jersey 10", sans-serif;
    font-size: 1.6rem;
    margin-bottom: 30px;
    letter-spacing: 1.4px;
  }

  .newsletter-form {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 18px;
    margin-bottom: 18px;
  }

  .newsletter-input-field {
    padding: 18px 32px;
    font-size: 1.4rem;
    border: none;
    border-radius: 0;
    background: var(--footer-text);
    color: var(--extra-color);
    font-family: "Jersey 10", sans-serif;
    width: 420px;
  }

  .newsletter-signup-btn {
    padding: 0.4rem 3rem;
    font-size: 1.4rem;
    border-radius: 0;
    background: var(--background-color);
    color: var(--extra-color);
    font-family: "Jersey 10", sans-serif;
    letter-spacing: 1px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: background 0.7s, color 0.7s;
  }
  
  .newsletter-signup-btn:hover {
    background: var(--paragraph-color);
    color: var(--background-color);
    border-right: 1.4px solid var(--extra-color);
  }

  .newsletter-privacy {
    font-size: 1.2rem;
    letter-spacing: 7px;
    opacity: 0.7;
    margin-top: 18px;
    font-family: "Jersey 10", sans-serif;
  }

  /* Black footer bar stuck at bottom */
  .business-footer {
    background: var(--background-color);
    color: var(--text-color);
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 10;
    padding: 0;
    font-family: "Jersey 10", sans-serif;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform: translateY(100%);
    opacity: 0;
  }
  .business-footer.footer-visible {
    transform: translateY(0);
    opacity: 1;
  }

  .footer-spacer {
    height: 88px; /* Adjust to match actual footer height */
    width: 100%;
  }

  .footer-bottom-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 0 18px 0;
  }

  .footer-links-row {
    display: flex;
    justify-content: space-between; /* Distribute left, center, and right sections */
    align-items: center;
    list-style: none;
    margin: 2.8rem 0;
    padding: 0;
  }

  .footer-links-left,
  .footer-links-right {
    padding: 1rem 3rem;
    font-size: 1.4rem;
    margin: 0 2rem;
    display: flex;
    gap: 2rem; /* Adjust spacing between links */
  }

  .footer-links-right a {
    margin: 0 5rem;
    transition: background-color 0.7s, color 0.7s;
    padding: 0.4rem 1.4rem;
  }

  .footer-links-left a {
    margin: 0 5rem;
    transition: background-color 0.7s, color 0.7s;
    padding: 0.4rem 1.4rem;
  }

  .footer-links-right:hover a {
    background-color: var(--extra-color);
    color: var(--text-color);
  }

  .footer-links-left:hover a {
    background-color: var(--extra-color);
    color: var(--text-color);
  }

  .footer-logo {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .footer-logo img {
    width: 80px; /* Adjust size as needed */
    height: auto; /* Maintain aspect ratio */
  }

  @media (max-width: 992px) {
    .footer-links-row {
      gap: 24px;
    }
    .newsletter-input-field, .newsletter-signup-btn {
      padding: 12px 18px;
      font-size: 1rem;
      width: 180px;
    }
  }

  @media (max-width: 576px) {
    .footer-links-row {
      flex-direction: column;
      gap: 8px;
    }
    .footer-logo {
      font-size: 2.2rem;
      width: 44px;
      height: 44px;
      line-height: 44px;
    }
    .newsletter-section {
      padding: 32px 0 18px 0;
    }
  }
/* Bottom Bar */
.footer-bottom {
  border-top: 1px solid rgba(146, 20, 12, 0.06);
  padding: 25px 0;
  font-size: 0.85rem;
  opacity: 0.6;
}

/* Responsive */
@media (max-width: 992px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .social-links {
    justify-content: center;
  }
  .footer-links a:hover {
    padding-left: 0;
  }
}
</style>