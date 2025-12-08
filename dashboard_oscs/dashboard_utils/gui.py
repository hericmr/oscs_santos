
import streamlit as st
import streamlit.components.v1 as components

def inject_mobile_detection():
    """
    Injects JavaScript to detect screen width and sets a 'mobile' query parameter
    if the width is below 700px. This allows Python to know the device state
    without complex bidirectional components.
    """
    js = """
    <script>
    function checkWidth() {
        try {
            const width = window.parent.innerWidth;
            const isMobile = width < 700;
            const urlParams = new URLSearchParams(window.parent.location.search);
            const currentMobile = urlParams.get('mobile');
            
            // Only reload if state changes between Desktop and Mobile
            // This prevents infinite reloads as long as we stay in the same mode
            if (isMobile && currentMobile !== 'true') {
                urlParams.set('mobile', 'true');
                window.parent.location.search = urlParams.toString();
            } else if (!isMobile && currentMobile === 'true') {
                urlParams.delete('mobile');
                window.parent.location.search = urlParams.toString();
            }
        } catch(e) {
            console.log("Error detecting width: " + e);
        }
    }
    
    // Check on load and resize
    checkWidth();
    // Add debounced listener if possible, but for simplicity direct listener
    // The checkWidth function only acts if state CHANGES, so standard resize is fine.
    window.addEventListener('resize', checkWidth);
    </script>
    """
    components.html(js, height=0)

def is_mobile_device():
    """
    Returns True if the 'mobile' query parameter is set to 'true'.
    Updates session_state['is_mobile'] available for other parts of the app.
    """
    # Read query params safely
    try:
        # Streamlit 1.30+
        if hasattr(st, "query_params"):
            is_mobile = st.query_params.get("mobile") == "true"
        else:
             # Fallback for older versions (though st.navigation implies new version)
            is_mobile = st.experimental_get_query_params().get("mobile", ["false"])[0] == "true"
    except Exception:
        is_mobile = False
        
    st.session_state['is_mobile'] = is_mobile
    return is_mobile

@st.dialog("Menu de Navegação")
def mobile_menu_dialog(pages):
    """
    Renders the mobile menu inside a dialog (modal).
    """
    st.write("Navegue pelas páginas:")
    for page in pages:
        # Use page_link for navigation
        st.page_link(page, label=page.title, icon=":material/arrow_forward:")
    
    # Close button is handled by the X, but we can add one
    if st.button("Fechar Menu", use_container_width=True):
        st.rerun()

def render_mobile_header(pages):
    """
    Renders the hamburger menu button for mobile.
    """
    # Simple top bar container
    # Uses columns to position button on the right or left?
    # User said: "Incluir um botão visível no topo, estilo “☰ Menu”"
    
    # We create a container to hold this header
    with st.container():
        col1, col2 = st.columns([0.80, 0.20])
        with col2:
            # Hamburger button
            if st.button("☰ Menu", key="mobile_menu_btn", help="Abrir Menu de Navegação", use_container_width=True):
                mobile_menu_dialog(pages)
        st.divider()
