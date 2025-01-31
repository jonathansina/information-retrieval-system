# class HeatmapAnalysis(DataAnalysis):
#     def _create_trace(self, **kwargs) -> go.Heatmap:
#         heatmap_plot_fig = px.imshow(
#             kwargs["corr_matrix"],
#             text_auto=True,
#             aspect="auto",
#             color_continuous_scale="Viridis",
#             title="نقشه حرارتی همبستگی ویژگی‌ها",
#             x=kwargs["features"],
#             y=kwargs["features"]
#         )
        
#         return heatmap_plot_fig
    
#     def _create_layout(self) -> Dict[str, Any]:
#         layout_config = {
#             "autosize": False,
#             "width": 1000,
#             "height": 800,
#             "margin": dict(l=50, r=50, b=50, t=50, pad=4),
#             "font": dict(
#                 family="B koodak, sans-serif",
#                 size=14,
#                 color="black"
#             ),
#             "title": {
#                 'text': "نقشه حرارتی همبستگی ویژگی‌ها",
#                 'y': 0.98,
#                 'x': 0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'
#             }
#         }

#         return layout_config
    
#     def plot(self) -> "HeatmapAnalysis":
#         self.fig = self._create_trace(
#             corr_matrix=self.dataframe.corr(),
#             features=list(self.dataframe.columns)
#         )
        
#         layout_config = self._create_layout()
#         self.fig.update_layout(layout_config)
        
#         self.fig.update_traces(
#             hovertemplate="<b>%{x} - %{y}</b><br>همبستگی: %{z:.2f}<extra></extra>",
#             texttemplate="%{z:.2f}",
#             hoverlabel=dict(
#                 font=dict(
#                     family="B koodak, sans-serif",
#                     size=14,
#                     color="white"
#                 )
#             )
#         )
        
#         return self