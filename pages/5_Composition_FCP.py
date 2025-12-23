import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration de la page
st.set_page_config(
    page_title="Composition FCP",
    page_icon="🥧",
    layout="wide"
)

# Constantes
DATA_FILE = os.getenv('FCP_DATA_FILE', 'data_fcp.xlsx')
PRIMARY_COLOR = "#004080"
SECONDARY_COLOR = "#333333"

# CSS personnalisé
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {PRIMARY_COLOR};
        text-align: center;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {PRIMARY_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_composition_data():
    """Charge les données de composition"""
    try:
        df = pd.read_excel(DATA_FILE, sheet_name='Composition FCP')
        if df.empty:
            st.error("La feuille 'Composition FCP' est vide.")
            return pd.DataFrame()
        return df
    except FileNotFoundError:
        st.error(f"Fichier {DATA_FILE} introuvable.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement de la composition: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_benchmarks():
    """Charge les données des benchmarks"""
    try:
        df = pd.read_excel(DATA_FILE, sheet_name='Benchmarks')
        if df.empty:
            st.error("La feuille 'Benchmarks' est vide.")
            return pd.DataFrame()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Fichier {DATA_FILE} introuvable.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des benchmarks: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_vl_data():
    """Charge les valeurs liquidatives"""
    try:
        df = pd.read_excel(DATA_FILE, sheet_name='Valeurs Liquidatives')
        if df.empty:
            st.error("La feuille 'Valeurs Liquidatives' est vide.")
            return pd.DataFrame()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Fichier {DATA_FILE} introuvable.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des valeurs liquidatives: {str(e)}")
        return pd.DataFrame()

# Application principale
def main():
    st.markdown('<h1 class="main-header">🥧 Composition des FCP</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Cette page présente la composition détaillée des Fonds Communs de Placement (FCP) et leur comparaison 
    avec les benchmarks de marché.
    """)
    
    # Chargement des données
    with st.spinner('Chargement des données...'):
        df_composition = load_composition_data()
        df_benchmarks = load_benchmarks()
        df_vl = load_vl_data()
    
    # Vérifier que les données sont chargées
    if df_composition.empty or df_benchmarks.empty or df_vl.empty:
        st.error("Impossible de charger les données. Veuillez vérifier que le fichier data_fcp.xlsx contient toutes les feuilles requises.")
        return
    
    # Obtenir la liste des FCPs
    fcps = sorted(df_composition['FCP'].unique())
    
    if len(fcps) == 0:
        st.error("Aucun FCP trouvé dans les données de composition.")
        return
    
    st.markdown("---")
    
    # Section 1: Sélection du FCP
    st.subheader("📊 Analyse de Composition")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_fcp = st.selectbox(
            "Sélectionnez un FCP",
            options=fcps,
            help="Choisissez le FCP dont vous souhaitez analyser la composition"
        )
        
        # Informations du FCP
        fcp_data = df_composition[df_composition['FCP'] == selected_fcp]
        
        if fcp_data.empty:
            st.error(f"Aucune donnée de composition trouvée pour {selected_fcp}")
            return
            
        fcp_type = fcp_data['Type FCP'].iloc[0]
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{selected_fcp}</h3>
            <p><strong>Type:</strong> {fcp_type}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Allocation par classe
        st.markdown("#### Allocation par Classe")
        allocation_classe = fcp_data.groupby('Classe')['Pourcentage'].sum().reset_index()
        allocation_classe = allocation_classe.sort_values('Pourcentage', ascending=False)
        
        for _, row in allocation_classe.iterrows():
            st.metric(row['Classe'], f"{row['Pourcentage']:.1f}%")
    
    with col2:
        # Onglets pour différentes visualisations
        tab1, tab2, tab3 = st.tabs(["🌳 Treemap", "☀️ Sunburst", "📊 Détails"])
        
        with tab1:
            st.markdown("##### Vue Hiérarchique - Treemap")
            
            # Préparer les données pour le treemap
            treemap_data = fcp_data.copy()
            treemap_data = treemap_data[treemap_data['Pourcentage'] > 0.01]  # Filtrer petites valeurs
            
            # Créer une hiérarchie pour le treemap
            treemap_data['Label'] = treemap_data.apply(
                lambda row: f"{row['Classe']}",
                axis=1
            )
            
            # Ajouter des détails selon la classe
            treemap_data['Detail'] = treemap_data.apply(
                lambda row: (
                    f"{row['Secteur']} - {row['Pays']}" if row['Classe'] == 'Actions' and pd.notna(row['Secteur'])
                    else f"{row['Secteur Obligation']} - {row['Pays']} ({row['Cotation']})" if row['Classe'] == 'Obligations' and pd.notna(row['Secteur Obligation'])
                    else row['Classe']
                ),
                axis=1
            )
            
            # Créer le treemap
            fig_treemap = px.treemap(
                treemap_data,
                path=['Label', 'Detail'],
                values='Pourcentage',
                title=f'Composition de {selected_fcp}',
                color='Pourcentage',
                color_continuous_scale='Blues',
                height=600
            )
            
            fig_treemap.update_traces(
                textinfo="label+percent parent",
                hovertemplate='<b>%{label}</b><br>Pourcentage: %{value:.2f}%<extra></extra>'
            )
            
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        with tab2:
            st.markdown("##### Vue Radiale - Sunburst")
            
            # Préparer les données pour le sunburst
            sunburst_data = fcp_data.copy()
            sunburst_data = sunburst_data[sunburst_data['Pourcentage'] > 0.01]
            
            # Créer des chemins hiérarchiques
            sunburst_data['Path1'] = sunburst_data['Classe']
            sunburst_data['Path2'] = sunburst_data.apply(
                lambda row: (
                    f"{row['Secteur']}" if row['Classe'] == 'Actions' and pd.notna(row['Secteur'])
                    else f"{row['Secteur Obligation']}" if row['Classe'] == 'Obligations' and pd.notna(row['Secteur Obligation'])
                    else row['Classe']
                ),
                axis=1
            )
            sunburst_data['Path3'] = sunburst_data.apply(
                lambda row: (
                    f"{row['Pays']}" if pd.notna(row['Pays'])
                    else ""
                ),
                axis=1
            )
            
            # Créer le sunburst
            fig_sunburst = px.sunburst(
                sunburst_data,
                path=['Path1', 'Path2', 'Path3'],
                values='Pourcentage',
                title=f'Composition Radiale de {selected_fcp}',
                color='Pourcentage',
                color_continuous_scale='Viridis',
                height=600
            )
            
            fig_sunburst.update_traces(
                hovertemplate='<b>%{label}</b><br>Pourcentage: %{value:.2f}%<extra></extra>'
            )
            
            st.plotly_chart(fig_sunburst, use_container_width=True)
        
        with tab3:
            st.markdown("##### Composition Détaillée")
            
            # Afficher par classe
            for classe in allocation_classe['Classe']:
                with st.expander(f"{classe} ({allocation_classe[allocation_classe['Classe']==classe]['Pourcentage'].values[0]:.2f}%)"):
                    classe_data = fcp_data[fcp_data['Classe'] == classe].copy()
                    
                    if classe == 'Actions':
                        # Regrouper par secteur
                        secteur_data = classe_data.groupby('Secteur')['Pourcentage'].sum().reset_index()
                        secteur_data = secteur_data.sort_values('Pourcentage', ascending=False)
                        st.markdown("**Par Secteur:**")
                        st.dataframe(secteur_data, use_container_width=True, hide_index=True)
                        
                        # Regrouper par pays
                        pays_data = classe_data.groupby('Pays')['Pourcentage'].sum().reset_index()
                        pays_data = pays_data.sort_values('Pourcentage', ascending=False)
                        st.markdown("**Par Pays:**")
                        st.dataframe(pays_data, use_container_width=True, hide_index=True)
                    
                    elif classe == 'Obligations':
                        # Regrouper par secteur
                        secteur_data = classe_data.groupby('Secteur Obligation')['Pourcentage'].sum().reset_index()
                        secteur_data = secteur_data.sort_values('Pourcentage', ascending=False)
                        st.markdown("**Par Secteur:**")
                        st.dataframe(secteur_data, use_container_width=True, hide_index=True)
                        
                        # Regrouper par cotation
                        cotation_data = classe_data.groupby('Cotation')['Pourcentage'].sum().reset_index()
                        cotation_data = cotation_data.sort_values('Pourcentage', ascending=False)
                        st.markdown("**Par Cotation:**")
                        st.dataframe(cotation_data, use_container_width=True, hide_index=True)
                        
                        # Regrouper par pays
                        pays_data = classe_data.groupby('Pays')['Pourcentage'].sum().reset_index()
                        pays_data = pays_data.sort_values('Pourcentage', ascending=False)
                        st.markdown("**Par Pays:**")
                        st.dataframe(pays_data, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Section 2: Comparaison avec les Benchmarks
    st.subheader("📈 Comparaison avec les Benchmarks")
    
    st.markdown("""
    Comparaison des performances des sous-portefeuilles Actions et Obligations avec leurs benchmarks respectifs.
    """)
    
    # Calculer les allocations Actions et Obligations pour le FCP sélectionné
    actions_pct = fcp_data[fcp_data['Classe'] == 'Actions']['Pourcentage'].sum()
    obligations_pct = fcp_data[fcp_data['Classe'] == 'Obligations']['Pourcentage'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Allocation Actions", f"{actions_pct:.1f}%")
    with col2:
        st.metric("Allocation Obligations", f"{obligations_pct:.1f}%")
    with col3:
        fcp_type_display = fcp_data['Type FCP'].iloc[0]
        st.metric("Type de FCP", fcp_type_display)
    
    # Graphique de comparaison
    st.markdown("##### Performance vs Benchmarks")
    
    # Obtenir les données VL du FCP
    fcp_vl = df_vl[['Date', selected_fcp]].copy()
    fcp_vl = fcp_vl[fcp_vl[selected_fcp].notna()]
    fcp_vl = fcp_vl.rename(columns={selected_fcp: 'VL'})
    
    if len(fcp_vl) == 0:
        st.warning(f"Aucune donnée de valeur liquidative disponible pour {selected_fcp}")
    else:
        # Normaliser à 100 au début (avec vérification division par zéro)
        if fcp_vl['VL'].iloc[0] != 0:
            fcp_vl['VL_norm'] = (fcp_vl['VL'] / fcp_vl['VL'].iloc[0]) * 100
        else:
            st.error(f"La première valeur liquidative de {selected_fcp} est zéro.")
            return
        
        # Normaliser les benchmarks à partir de la date de début du FCP
        bench_data = df_benchmarks[df_benchmarks['Date'] >= fcp_vl['Date'].min()].copy()
        
        if len(bench_data) == 0:
            st.warning("Aucune donnée de benchmark disponible pour la période du FCP")
        else:
            # Vérifier et normaliser les benchmarks
            if bench_data['Benchmark Obligataire'].iloc[0] != 0:
                bench_data['Bench_Oblig_norm'] = (bench_data['Benchmark Obligataire'] / bench_data['Benchmark Obligataire'].iloc[0]) * 100
            else:
                bench_data['Bench_Oblig_norm'] = 100
                
            if bench_data['Benchmark Actions'].iloc[0] != 0:
                bench_data['Bench_Actions_norm'] = (bench_data['Benchmark Actions'] / bench_data['Benchmark Actions'].iloc[0]) * 100
            else:
                bench_data['Bench_Actions_norm'] = 100
            
            # Créer le graphique
            fig_bench = go.Figure()
            
            fig_bench.add_trace(go.Scatter(
                x=fcp_vl['Date'],
                y=fcp_vl['VL_norm'],
                name=selected_fcp,
                line=dict(color=PRIMARY_COLOR, width=3)
            ))
            
            if actions_pct > 0:
                fig_bench.add_trace(go.Scatter(
                    x=bench_data['Date'],
                    y=bench_data['Bench_Actions_norm'],
                    name='Benchmark Actions',
                    line=dict(color='green', width=2, dash='dash')
                ))
            
            if obligations_pct > 0:
                fig_bench.add_trace(go.Scatter(
                    x=bench_data['Date'],
                    y=bench_data['Bench_Oblig_norm'],
                    name='Benchmark Obligataire',
                    line=dict(color='orange', width=2, dash='dash')
                ))
            
            fig_bench.update_layout(
                title=f'Performance de {selected_fcp} vs Benchmarks (base 100)',
                xaxis_title='Date',
                yaxis_title='Performance Indexée (base 100)',
                hovermode='x unified',
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_bench, use_container_width=True)
            
            st.plotly_chart(fig_bench, use_container_width=True)
            
            # Statistiques de performance
            st.markdown("##### Statistiques de Performance")
            
            # Calculer les rendements avec vérification
            if len(fcp_vl) > 0 and fcp_vl['VL'].iloc[0] != 0 and fcp_vl['VL'].iloc[-1] != 0:
                fcp_return = ((fcp_vl['VL'].iloc[-1] / fcp_vl['VL'].iloc[0]) - 1) * 100
            else:
                fcp_return = 0.0
                
            if len(bench_data) > 0:
                if bench_data['Benchmark Obligataire'].iloc[0] != 0 and bench_data['Benchmark Obligataire'].iloc[-1] != 0:
                    bench_oblig_return = ((bench_data['Benchmark Obligataire'].iloc[-1] / bench_data['Benchmark Obligataire'].iloc[0]) - 1) * 100
                else:
                    bench_oblig_return = 0.0
                    
                if bench_data['Benchmark Actions'].iloc[0] != 0 and bench_data['Benchmark Actions'].iloc[-1] != 0:
                    bench_actions_return = ((bench_data['Benchmark Actions'].iloc[-1] / bench_data['Benchmark Actions'].iloc[0]) - 1) * 100
                else:
                    bench_actions_return = 0.0
            else:
                bench_oblig_return = 0.0
                bench_actions_return = 0.0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    f"Rendement {selected_fcp}",
                    f"{fcp_return:.2f}%",
                    help=f"Rendement cumulé depuis {fcp_vl['Date'].min().strftime('%Y-%m-%d')}"
                )
            
            with col2:
                if obligations_pct > 0:
                    st.metric(
                        "Benchmark Obligataire",
                        f"{bench_oblig_return:.2f}%",
                        delta=f"{fcp_return - bench_oblig_return:.2f}% vs FCP",
                        help="Rendement du benchmark obligataire sur la même période"
                    )
            
            with col3:
                if actions_pct > 0:
                    st.metric(
                        "Benchmark Actions",
                        f"{bench_actions_return:.2f}%",
                        delta=f"{fcp_return - bench_actions_return:.2f}% vs FCP",
                        help="Rendement du benchmark actions sur la même période"
                    )
    
    st.markdown("---")
    
    # Section 3: Vue d'ensemble de tous les FCPs
    st.subheader("🎯 Vue d'Ensemble - Tous les FCPs")
    
    # Créer un résumé par FCP
    summary_data = []
    for fcp in fcps:
        fcp_comp = df_composition[df_composition['FCP'] == fcp]
        summary_data.append({
            'FCP': fcp,
            'Type': fcp_comp['Type FCP'].iloc[0],
            'Actions (%)': fcp_comp[fcp_comp['Classe'] == 'Actions']['Pourcentage'].sum(),
            'Obligations (%)': fcp_comp[fcp_comp['Classe'] == 'Obligations']['Pourcentage'].sum(),
            'OPCVM (%)': fcp_comp[fcp_comp['Classe'] == 'OPCVM']['Pourcentage'].sum(),
            'Liquidités (%)': fcp_comp[fcp_comp['Classe'] == 'Liquidités']['Pourcentage'].sum()
        })
    
    df_summary = pd.DataFrame(summary_data)
    
    # Graphique par type de FCP
    fig_types = px.bar(
        df_summary,
        x='FCP',
        y=['Actions (%)', 'Obligations (%)', 'OPCVM (%)', 'Liquidités (%)'],
        title='Allocation par Classe d\'Actifs - Tous les FCPs',
        labels={'value': 'Pourcentage (%)', 'variable': 'Classe d\'Actifs'},
        color_discrete_map={
            'Actions (%)': 'green',
            'Obligations (%)': 'orange',
            'OPCVM (%)': 'blue',
            'Liquidités (%)': 'gray'
        },
        height=500
    )
    
    fig_types.update_layout(
        xaxis_tickangle=-45,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_types, use_container_width=True)
    
    # Tableau récapitulatif
    st.markdown("##### Tableau Récapitulatif")
    
    # Ajouter des couleurs conditionnelles
    st.dataframe(
        df_summary.style.format({
            'Actions (%)': '{:.1f}',
            'Obligations (%)': '{:.1f}',
            'OPCVM (%)': '{:.1f}',
            'Liquidités (%)': '{:.1f}'
        }).background_gradient(subset=['Actions (%)', 'Obligations (%)'], cmap='RdYlGn', vmin=0, vmax=100),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Informations complémentaires
    with st.expander("ℹ️ À propos de cette page"):
        st.markdown("""
        ### Composition des FCP
        
        Cette page présente la composition détaillée des Fonds Communs de Placement selon:
        
        **Types de FCP:**
        - **Obligataires**: Investissent principalement en obligations (60-80%)
        - **Actions**: Investissent principalement en actions (60-80%)
        - **Diversifiés**: Allocation équilibrée entre actions et obligations (30-50% chacun)
        
        **Classes d'Actifs:**
        - **Actions**: Réparties par secteur (Agriculture, Distribution, Finance, etc.) et par pays (zone UEMOA)
        - **Obligations**: Réparties par secteur (Etat, Institutionnel, Regional), pays et cotation
        - **OPCVM**: Investissements dans d'autres fonds
        - **Liquidités**: Trésorerie et équivalents
        
        **Benchmarks:**
        - **Benchmark Obligataire**: Indice de référence pour les obligations
        - **Benchmark Actions**: Indice de référence pour les actions
        
        Les visualisations (Treemap et Sunburst) permettent d'explorer la composition de manière interactive.
        """)

if __name__ == "__main__":
    main()
