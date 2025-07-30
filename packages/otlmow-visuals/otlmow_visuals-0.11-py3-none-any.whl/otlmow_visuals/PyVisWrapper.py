import base64
import json
import re
import warnings
import webbrowser
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from random import choice
from typing import Optional


from otlmow_model.OtlmowModel.BaseClasses.OTLObject import OTLObject
from otlmow_model.OtlmowModel.BaseClasses.RelationInteractor import RelationInteractor
from otlmow_model.OtlmowModel.Classes.Agent import Agent
from otlmow_model.OtlmowModel.Classes.ImplementatieElement.AIMObject import AIMObject
from otlmow_model.OtlmowModel.Helpers import OTLObjectHelper
from otlmow_model.OtlmowModel.Helpers.OTLObjectHelper import is_relation, is_directional_relation
from pyvis import network as pyvis_network
import networkx as nx

class PyVisWrapper:
    max_screen_name_char_count = 17
    def __init__(self, notebook_mode: bool = False):
        self.special_nodes = []
        self.special_edges = []
        self.relation_id_to_collection_id: dict[str,list] = defaultdict(list)
        self.collection_id_to_list_of_relation_ids:dict[str,list[str]] = defaultdict(list)
        self.asset_id_to_display_name_dict = {}
        self.relation_id_to_subedges = defaultdict(list)
        self.relation_id_to_joint_nodes = defaultdict(list)
        self.collection_relation_count_threshold = 10
        # relations removed from initial data because they are put into a collection
        # but added again after stabilizing
        # are only visible when you hover over the collection
        self.collection_relations_id_to_relation_data: dict[str,str] ={}

        if notebook_mode:
            warnings.warn("set the nodebook mode using the show method")
        self.notebook_mode = notebook_mode
        self.relatie_color_dict = {
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBetrokkene': 'f59900',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#VoedtAangestuurd': 'c71585',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftNetwerkProtectie': 'ffa500',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IsAdmOnderdeelVan': 'f08080',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Voedt': 'ff0000',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IsSWOnderdeelVan': '800080',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IsSWGehostOp': '0000ff',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing': '008000',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IsNetwerkECC': '8a2be2',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging': '000000',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#LigtOp': '32cd32',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#SluitAanOp': '1e90ff',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBeheer': 'bc8f8f',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HoortBij': 'cc5416',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftNetwerktoegang': 'ee82ee',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#IsInspectieVan': '66d5f5',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#RelatieObject': 'f59900',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Omhult': '800000',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftAanvullendeGeometrie': '9400d3',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftToegangsprocedure': 'a52a2a',
            'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBijlage': '0000ff',
        }
        self.awv_color_list = ("#7F4C32","#6A3D9A","#FF7F00","#33A02C","#1F78B4","#E31A1C",
                               "#B8B327","#CAB2D6","#FDBF6F","#B2DF8A","#A6CEE3","#FB9A99")
        self.list_of_colors = (
            "#E5E5E5", "#CCCCCC", "#B2B2B2", "#999999", "#808080", "#666666", "#4D4D4D", "#333333", "#E8E3E3",
            "#EBE0E0", "#EDDEDE", "#F0DBDB", "#F2D9D9", "#F5D6D6", "#F7D4D4", "#FAD1D1", "#FCCFCF", "#FFCCCC",
            "#D1C7C7", "#D6C2C2", "#DBBDBD", "#E0B8B8", "#E6B3B3", "#EBADAD", "#F0A8A8", "#F5A3A3", "#FA9E9E",
            "#FF9999", "#BAABAB", "#C2A3A3", "#C99C9C", "#D19494", "#D98C8C", "#E08585", "#E87D7D", "#F07575",
            "#F76E6E", "#FF6666", "#A38F8F", "#AD8585", "#B87A7A", "#C27070", "#CC6666", "#D65C5C", "#E05252",
            "#EB4747", "#F53D3D", "#FF3333", "#8C7373", "#996666", "#A65959", "#B24D4D", "#BF4040", "#CC3333",
            "#D92626", "#E61919", "#F20D0D", "#FF0000", "#705C5C", "#7A5252", "#854747", "#8F3D3D", "#993333",
            "#A32929", "#AD1F1F", "#B81414", "#C20A0A", "#CC0000", "#544545", "#5C3D3D", "#633636", "#6B2E2E",
            "#732626", "#7A1F1F", "#821717", "#8A0F0F", "#910808", "#990000", "#382E2E", "#3D2929", "#422424",
            "#471F1F", "#4D1919", "#521414", "#570F0F", "#5C0A0A", "#610505", "#660000", "#E8E6E3", "#EBE6E0",
            "#EDE6DE", "#F0E6DB", "#F2E6D9", "#F5E6D6", "#F7E6D4", "#FAE6D1", "#FCE6CF", "#FFE6CC", "#D1CCC7",
            "#D6CCC2", "#DBCCBD", "#E0CCB8", "#E6CCB3", "#EBCCAD", "#F0CCA8", "#F5CCA3", "#FACC9E", "#FFCC99",
            "#BAB2AB", "#C2B2A3", "#C9B29C", "#D1B294", "#D9B28C", "#E0B285", "#E8B27D", "#F0B275", "#F7B26E",
            "#FFB266", "#A3998F", "#AD9985", "#B8997A", "#C29970", "#CC9966", "#D6995C", "#E09952", "#EB9947",
            "#F5993D", "#FF9933", "#8C8073", "#998066", "#A68059", "#B2804D", "#BF8040", "#CC8033", "#D98026",
            "#E68019", "#F2800D", "#FF8000", "#70665C", "#7A6652", "#856647", "#8F663D", "#996633", "#A36629",
            "#AD661F", "#B86614", "#C2660A", "#CC6600", "#544C45", "#5C4C3D", "#634C36", "#6B4C2E", "#734C26",
            "#7A4C1F", "#824C17", "#8A4C0F", "#914C08", "#994C00", "#38332E", "#3D3329", "#423324", "#47331F",
            "#4D3319", "#523314", "#57330F", "#5C330A", "#613305", "#663300", "#E8E8E3", "#EBEBE0", "#EDEDDE",
            "#F0F0DB", "#F2F2D9", "#F5F5D6", "#F7F7D4", "#FAFAD1", "#FCFCCF", "#FFFFCC", "#D1D1C7", "#D6D6C2",
            "#DBDBBD", "#E0E0B8", "#E6E6B3", "#EBEBAD", "#F0F0A8", "#F5F5A3", "#FAFA9E", "#FFFF99", "#BABAAB",
            "#C2C2A3", "#C9C99C", "#D1D194", "#D9D98C", "#E0E085", "#E8E87D", "#F0F075", "#F7F76E", "#FFFF66",
            "#A3A38F", "#ADAD85", "#B8B87A", "#C2C270", "#CCCC66", "#D6D65C", "#E0E052", "#EBEB47", "#F5F53D",
            "#FFFF33", "#8C8C73", "#999966", "#A6A659", "#B2B24D", "#BFBF40", "#CCCC33", "#D9D926", "#E5E619",
            "#F2F20D", "#FFFF00", "#70705C", "#7A7A52", "#858547", "#8F8F3D", "#999933", "#A3A329", "#ADAD1F",
            "#B8B814", "#C2C20A", "#CCCC00", "#545445", "#5C5C3D", "#636336", "#6B6B2E", "#737326", "#7A7A1F",
            "#828217", "#8A8A0F", "#919108", "#999900", "#38382E", "#3D3D29", "#424224", "#47471F", "#4C4D19",
            "#525214", "#57570F", "#5C5C0A", "#616105", "#666600", "#E6E8E3", "#E6EBE0", "#E6EDDE", "#E6F0DB",
            "#E6F2D9", "#E6F5D6", "#E6F7D4", "#E6FAD1", "#E6FCCF", "#E6FFCC", "#CCD1C7", "#CCD6C2", "#CCDBBD",
            "#CCE0B8", "#CCE6B3", "#CCEBAD", "#CCF0A8", "#CCF5A3", "#CCFA9E", "#CCFF99", "#B2BAAB", "#B2C2A3",
            "#B2C99C", "#B2D194", "#B3D98C", "#B3E085", "#B3E87D", "#B3F075", "#B3F76E", "#B3FF66", "#99A38F",
            "#99AD85", "#99B87A", "#99C270", "#99CC66", "#99D65C", "#99E052", "#99EB47", "#99F53D", "#99FF33",
            "#808C73", "#809966", "#80A659", "#80B24D", "#80BF40", "#80CC33", "#80D926", "#80E619", "#80F20D",
            "#80FF00", "#66705C", "#667A52", "#668547", "#668F3D", "#669933", "#66A329", "#66AD1F", "#66B814",
            "#66C20A", "#66CC00", "#4C5445", "#4C5C3D", "#4D6336", "#4D6B2E", "#4D7326", "#4D7A1F", "#4D8217",
            "#4D8A0F", "#4D9108", "#4D9900", "#33382E", "#333D29", "#334224", "#33471F", "#334D19", "#335214",
            "#33570F", "#335C0A", "#336105", "#336600", "#E3E8E3", "#E0EBE0", "#DEEDDE", "#DBF0DB", "#D9F2D9",
            "#D6F5D6", "#D4F7D4", "#D1FAD1", "#CFFCCF", "#CCFFCC", "#C7D1C7", "#C2D6C2", "#BDDBBD", "#B8E0B8",
            "#B3E6B3", "#ADEBAD", "#A8F0A8", "#A3F5A3", "#9EFA9E", "#99FF99", "#ABBAAB", "#A3C2A3", "#9CC99C",
            "#94D194", "#8CD98C", "#85E085", "#7DE87D", "#75F075", "#6EF76E", "#66FF66", "#8FA38F", "#85AD85",
            "#7AB87A", "#70C270", "#66CC66", "#5CD65C", "#52E052", "#47EB47", "#3DF53D", "#33FF33", "#738C73",
            "#669966", "#59A659", "#4DB24D", "#40BF40", "#33CC33", "#26D926", "#19E619", "#0DF20D", "#00FF00",
            "#5C705C", "#527A52", "#478547", "#3D8F3D", "#339933", "#29A329", "#1FAD1F", "#14B814", "#0AC20A",
            "#00CC00", "#455445", "#3D5C3D", "#366336", "#2E6B2E", "#267326", "#1F7A1F", "#178217", "#0F8A0F",
            "#089108", "#009900", "#2E382E", "#293D29", "#244224", "#1F471F", "#194D19", "#145214", "#0F570F",
            "#0A5C0A", "#056105", "#006600", "#E3E8E6", "#E0EBE6", "#DEEDE6", "#DBF0E6", "#D9F2E6", "#D6F5E6",
            "#D4F7E6", "#D1FAE6", "#CFFCE6", "#CCFFE6", "#C7D1CC", "#C2D6CC", "#BDDBCC", "#B8E0CC", "#B3E6CC",
            "#ADEBCC", "#A8F0CC", "#A3F5CC", "#9EFACC", "#99FFCC", "#ABBAB2", "#A3C2B2", "#9CC9B2", "#94D1B2",
            "#8CD9B3", "#85E0B3", "#7DE8B3", "#75F0B3", "#6EF7B3", "#66FFB3", "#8FA399", "#85AD99", "#7AB899",
            "#70C299", "#66CC99", "#5CD699", "#52E099", "#47EB99", "#3DF599", "#33FF99", "#738C80", "#669980",
            "#59A680", "#4DB280", "#40BF80", "#33CC80", "#26D980", "#19E680", "#0DF280", "#00FF80", "#5C7066",
            "#527A66", "#478566", "#3D8F66", "#339966", "#29A366", "#1FAD66", "#14B866", "#0AC266", "#00CC66",
            "#45544C", "#3D5C4C", "#36634D", "#2E6B4D", "#26734D", "#1F7A4D", "#17824D", "#0F8A4D", "#08914D",
            "#00994D", "#2E3833", "#293D33", "#244233", "#1F4733", "#194D33", "#145233", "#0F5733", "#0A5C33",
            "#056133", "#006633", "#E3E8E8", "#E0EBEB", "#DEEDED", "#DBF0F0", "#D9F2F2", "#D6F5F5", "#D4F7F7",
            "#D1FAFA", "#CFFCFC", "#CCFFFF", "#C7D1D1", "#C2D6D6", "#BDDBDB", "#B8E0E0", "#B3E6E6", "#ADEBEB",
            "#A8F0F0", "#A3F5F5", "#9EFAFA", "#99FFFF", "#ABBABA", "#A3C2C2", "#9CC9C9", "#94D1D1", "#8CD9D9",
            "#85E0E0", "#7DE8E8", "#75F0F0", "#6EF7F7", "#66FFFF", "#8FA3A3", "#85ADAD", "#7AB8B8", "#70C2C2",
            "#66CCCC", "#5CD6D6", "#52E0E0", "#47EBEB", "#3DF5F5", "#33FFFF", "#738C8C", "#669999", "#59A6A6",
            "#4DB2B2", "#40BFBF", "#33CCCC", "#26D9D9", "#19E5E6", "#0DF2F2", "#00FFFF", "#5C7070", "#527A7A",
            "#478585", "#3D8F8F", "#339999", "#29A3A3", "#1FADAD", "#14B8B8", "#0AC2C2", "#00CCCC", "#455454",
            "#3D5C5C", "#366363", "#2E6B6B", "#267373", "#1F7A7A", "#178282", "#0F8A8A", "#089191", "#009999",
            "#2E3838", "#293D3D", "#244242", "#1F4747", "#194C4D", "#145252", "#0F5757", "#0A5C5C", "#056161",
            "#006666", "#E3E6E8", "#E0E6EB", "#DEE6ED", "#DBE6F0", "#D9E6F2", "#D6E6F5", "#D4E5F7", "#D1E5FA",
            "#CFE5FC", "#CCE5FF", "#C7CCD1", "#C2CCD6", "#BDCCDB", "#B8CCE0", "#B3CCE6", "#ADCCEB", "#A8CCF0",
            "#A3CCF5", "#9ECCFA", "#99CCFF", "#ABB2BA", "#A3B2C2", "#9CB2C9", "#94B2D1", "#8CB2D9", "#85B2E0",
            "#7DB2E8", "#75B2F0", "#6EB2F7", "#66B2FF", "#8F99A3", "#8599AD", "#7A99B8", "#7099C2", "#6699CC",
            "#5C99D6", "#5299E0", "#4799EB", "#3D99F5", "#3399FF", "#737F8C", "#667F99", "#597FA6", "#4D7FB2",
            "#407FBF", "#337FCC", "#267FD9", "#197FE6", "#0D7FF2", "#007FFF", "#5C6670", "#52667A", "#476685",
            "#3D668F", "#336699", "#2966A3", "#1F66AD", "#1466B8", "#0A66C2", "#0066CC", "#454C54", "#3D4C5C",
            "#364C63", "#2E4C6B", "#264C73", "#1F4C7A", "#174C82", "#0F4C8A", "#084C91", "#004C99", "#2E3338",
            "#29333D", "#243342", "#1F3347", "#19334D", "#143352", "#0F3357", "#0A335C", "#053361", "#003366",
            "#E3E3E8", "#E0E0EB", "#DEDEED", "#DBDBF0", "#D9D9F2", "#D6D6F5", "#D4D4F7", "#D1D1FA", "#CFCFFC",
            "#CCCCFF", "#C7C7D1", "#C2C2D6", "#BDBDDB", "#B8B8E0", "#B3B3E6", "#ADADEB", "#A8A8F0", "#A3A3F5",
            "#9E9EFA", "#9999FF", "#ABABBA", "#A3A3C2", "#9C9CC9", "#9494D1", "#8C8CD9", "#8585E0", "#7D7DE8",
            "#7575F0", "#6E6EF7", "#6666FF", "#8F8FA3", "#8585AD", "#7A7AB8", "#7070C2", "#6666CC", "#5C5CD6",
            "#5252E0", "#4747EB", "#3D3DF5", "#3333FF", "#73738C", "#666699", "#5959A6", "#4D4DB2", "#4040BF",
            "#3333CC", "#2626D9", "#1919E6", "#0D0DF2", "#0000FF", "#5C5C70", "#52527A", "#474785", "#3D3D8F",
            "#333399", "#2929A3", "#1F1FAD", "#1414B8", "#0A0AC2", "#0000CC", "#454554", "#3D3D5C", "#363663",
            "#2E2E6B", "#262673", "#1F1F7A", "#171782", "#0F0F8A", "#080891", "#000099", "#2E2E38", "#29293D",
            "#242442", "#1F1F47", "#19194D", "#141452", "#0F0F57", "#0A0A5C", "#050561", "#000066", "#E6E3E8",
            "#E6E0EB", "#E6DEED", "#E6DBF0", "#E6D9F2", "#E6D6F5", "#E5D4F7", "#E5D1FA", "#E5CFFC", "#E5CCFF",
            "#CCC7D1", "#CCC2D6", "#CCBDDB", "#CCB8E0", "#CCB3E6", "#CCADEB", "#CCA8F0", "#CCA3F5", "#CC9EFA",
            "#CC99FF", "#B2ABBA", "#B2A3C2", "#B29CC9", "#B294D1", "#B28CD9", "#B285E0", "#B27DE8", "#B275F0",
            "#B26EF7", "#B266FF", "#998FA3", "#9985AD", "#997AB8", "#9970C2", "#9966CC", "#995CD6", "#9952E0",
            "#9947EB", "#993DF5", "#9933FF", "#7F738C", "#7F6699", "#7F59A6", "#7F4DB2", "#7F40BF", "#7F33CC",
            "#7F26D9", "#7F19E6", "#7F0DF2", "#7F00FF", "#665C70", "#66527A", "#664785", "#663D8F", "#663399",
            "#6629A3", "#661FAD", "#6614B8", "#660AC2", "#6600CC", "#4C4554", "#4C3D5C", "#4C3663", "#4C2E6B",
            "#4C2673", "#4C1F7A", "#4C1782", "#4C0F8A", "#4C0891", "#4C0099", "#332E38", "#33293D", "#332442",
            "#331F47", "#33194D", "#331452", "#330F57", "#330A5C", "#330561", "#330066", "#E8E3E8", "#EBE0EB",
            "#EDDEED", "#F0DBF0", "#F2D9F2", "#F5D6F5", "#F7D4F7", "#FAD1FA", "#FCCFFC", "#FFCCFF", "#D1C7D1",
            "#D6C2D6", "#DBBDDB", "#E0B8E0", "#E6B3E6", "#EBADEB", "#F0A8F0", "#F5A3F5", "#FA9EFA", "#FF99FF",
            "#BAABBA", "#C2A3C2", "#C99CC9", "#D194D1", "#D98CD9", "#E085E0", "#E87DE8", "#F075F0", "#F76EF7",
            "#FF66FF", "#A38FA3", "#AD85AD", "#B87AB8", "#C270C2", "#CC66CC", "#D65CD6", "#E052E0", "#EB47EB",
            "#F53DF5", "#FF33FF", "#8C738C", "#996699", "#A659A6", "#B24DB2", "#BF40BF", "#CC33CC", "#D926D9",
            "#E619E5", "#F20DF2", "#FF00FF", "#705C70", "#7A527A", "#854785", "#8F3D8F", "#993399", "#A329A3",
            "#AD1FAD", "#B814B8", "#C20AC2", "#CC00CC", "#544554", "#5C3D5C", "#633663", "#6B2E6B", "#732673",
            "#7A1F7A", "#821782", "#8A0F8A", "#910891", "#990099", "#382E38", "#3D293D", "#422442", "#471F47",
            "#4D194C", "#521452", "#570F57", "#5C0A5C", "#610561", "#660066", "#E8E3E6", "#EBE0E6", "#EDDEE6",
            "#F0DBE6", "#F2D9E6", "#F5D6E6", "#F7D4E6", "#FAD1E6", "#FCCFE6", "#FFCCE6", "#D1C7CC", "#D6C2CC",
            "#DBBDCC", "#E0B8CC", "#E6B3CC", "#EBADCC", "#F0A8CC", "#F5A3CC", "#FA9ECC", "#FF99CC", "#BAABB2",
            "#C2A3B2", "#C99CB2", "#D194B2", "#D98CB3", "#E085B3", "#E87DB3", "#F075B3", "#F76EB3", "#FF66B3",
            "#A38F99", "#AD8599", "#B87A99", "#C27099", "#CC6699", "#D65C99", "#E05299", "#EB4799", "#F53D99",
            "#FF3399", "#8C7380", "#996680", "#A65980", "#B24D80", "#BF4080", "#CC3380", "#D92680", "#E61980",
            "#F20D80", "#FF0080", "#705C66", "#7A5266", "#854766", "#8F3D66", "#993366", "#A32966", "#AD1F66",
            "#B81466", "#C20A66", "#CC0066", "#54454C", "#5C3D4C", "#63364D", "#6B2E4D", "#73264D", "#7A1F4D",
            "#82174D", "#8A0F4D", "#91084D", "#99004D", "#382E33", "#3D2933", "#422433", "#471F33", "#4D1933",
            "#521433", "#570F33", "#5C0A33", "#610533", "#660033")



        self.color_dict = {}

    @classmethod
    def remove_duplicates_in_iterable_based_on_asset_id(self, list_of_objects: [OTLObject]) -> [
        OTLObject]:
        unique = {}
        for elem in list_of_objects:
            if elem.typeURI == 'http://purl.org/dc/terms/Agent':
                unique.setdefault(elem.agentId.identificator, elem)
            else:
                unique.setdefault(elem.assetId.identificator, elem)
        return list(unique.values())

    def show(self, list_of_objects: [OTLObject], html_path: Path = Path('example.html'), visualisation_option:int = 1, launch_html: bool = True,
             notebook_mode: bool = False,collection_threshold=-1, **kwargs) -> None:

        if collection_threshold == -1:
            collection_threshold = self.collection_relation_count_threshold


        if notebook_mode and kwargs.get('cdn_resources') != 'in_line':
            kwargs['cdn_resources'] = 'in_line'
        g = pyvis_network.Network(directed=True, notebook=notebook_mode, **kwargs)

        assets = []
        relations = []
        relations_per_asset_doel = defaultdict(list)
        relations_per_asset_bron = defaultdict(list)
        relations_per_asset_undirected = defaultdict(list)
        for o in list_of_objects:
            if is_relation(o):
                relations.append(o)
                if is_directional_relation(o):
                    self.add_object_to_ordering(o, relations_per_asset_doel,o.doelAssetId.identificator)
                    self.add_object_to_ordering(o, relations_per_asset_bron,o.bronAssetId.identificator)
                else:
                    self.add_object_to_ordering(o, relations_per_asset_undirected,
                                                o.doelAssetId.identificator)
                    self.add_object_to_ordering(o, relations_per_asset_undirected,
                                                o.bronAssetId.identificator)
            else:
                assets.append(o)

        nodes_created = self.create_nodes(g, assets)

        self.special_nodes = []
        self.special_edges = []
        # remove relations to asset that have to many relation create a new node with one relation
        self.create_special_nodes_and_relations(g=g, assets=assets, relations=relations,
                                                initial_relations_per_asset=relations_per_asset_doel,
                                                directed =True,
                                                collection_threshold=collection_threshold)
        self.create_special_nodes_and_relations(g=g, assets=assets, relations=relations,
                                                initial_relations_per_asset=relations_per_asset_bron,
                                                directed =True,use_bron=False,
                                                collection_threshold=collection_threshold)

        self.create_special_nodes_and_relations(g=g, assets=assets, relations=relations,
                                                initial_relations_per_asset=relations_per_asset_undirected,
                                                directed=False, use_bron=False,
                                                collection_threshold=collection_threshold)

        self.create_edges(g, list_of_objects=relations, nodes=nodes_created)

        # hierarchical + hierarchical repulse physics
        options_1_hierarchisch = ('options = {'
                      '"nodes": '
                      '{'
                      '      "font":'
                      '      {'
                      '           "size": 25,'
                      '           "color":"#000000" '
                      '       },'
                      '       "margin": 10,'
                      '       "widthConstraint":'
                      '       {   '
                      '           "minimum": 150,'
                      '           "maximum": 250'
                      '       }   '
                      '}, '
                      '"interaction": {"dragView": true,"hover":true, "selectConnectedEdges": false,"tooltipDelay":500}, '
                      ' "layout": '
                      '{'
                      '     "hierarchical": '
                      '     {'
                      '         "enabled": true,'
                      '         "levelSeparation": 290,'
                      '         "nodeSpacing": 467,'
                      '         "treeSpacing": 492,'
                      '         "edgeMinimization": false,'
                      '         "parentCentralization": false,'
                      '     "   direction": "LR"'
                      '     }'
                      '},'
                      '"physics": '
                      '{'
                      '     "hierarchicalRepulsion":    '
                      '     {'
                      '         "centralGravity": 1.05,'
                      '         "springLength": 170,'
                      '         "springConstant": 1,'
                      '         "nodeDistance": 90,'
                      '         "avoidOverlap": 1'
                      '     },'
                      '"minVelocity": 0.75,'
                      '"solver": "hierarchicalRepulsion",'
                        '"stabilization": '
                      '{'
                         ' "enabled": true,'
                          '"iterations": 1000,'
                          '"fit": true'
                      '   }'         
                      '}'
                '}')

        # special barneshut setting
        options_2_spiderweb = ('options = {'
                      '"nodes": '
                      '{'
                      '      "font":'
                      '      {'
                      '           "size": 25,'
                      '           "color":"#000000" '
                      '       },'
                      '       "margin": 10,'
                      '       "widthConstraint":'
                      '       {   '
                      '           "minimum": 150,'
                      '           "maximum": 250'
                      '       }   '
                      '}, '
                      '"interaction": {"dragView": true,"hover":true, "selectConnectedEdges": false,"tooltipDelay":500}, '
                      '"physics":'
                      '{'
                      '"barnesHut": '
                      '{'
                      '       "theta": 0.1, '
                      '       "gravitationalConstant": -475455,   '   
                      '       "centralGravity": 0.1,'
                      '       "springLength": 150,'
                      '       "springConstant": 22,'
                      '       "nodeDistance": 125,'
                      '       "damping": 0.73, '    
                      '       "avoidOverlap": 1'
                      '},'
                      '"minVelocity": 0.75,'
                      '"solver": "barnesHut"'
                      '},'
                      '"layout" : {'
                      '"clusterThreshold": 150'
                      ' },'
                      '"stabilization": '
                      '{'
                         ' "enabled": true,'
                          '"iterations": 1000,'
                          '"fit": true'
                      '   }'         

                      '}')

        # shell setting
        options_3_shell = ('options = {'
                              '"nodes": '
                              '{'
                              '      "font":'
                              '      {'
                              '           "size": 25,'
                              '           "color":"#000000" '
                              '       },'
                              '       "margin": 10,'
                              '       "widthConstraint":'
                              '       {   '
                              '           "minimum": 150,'
                              '           "maximum": 250'
                              '       }   '
                              '}, '
                              '"interaction": {"dragView": true,"hover":true, "selectConnectedEdges": false,"tooltipDelay":500}, '
                              '"physics":'
                              '{'
                              ' "enabled": false'
                              '}' 
                        '}')

        options_4_hierarch_repulsion = ('options = {'
                               '"nodes": '
                               '{'
                               '      "font":'
                               '      {'
                               '           "size": 25,'
                               '           "color":"#000000" '
                               '       },'
                               '       "margin": 10,'
                               '       "widthConstraint":'
                               '       {   '
                               '           "minimum": 150,'
                               '           "maximum": 250'
                               '       }   '
                               '}, '
                               '"interaction": {"dragView": true,"hover":true, "selectConnectedEdges": false,"tooltipDelay":500}, '
                               ' "physics": {'
                               '     "hierarchicalRepulsion": {'
                               '     "centralGravity": 9.45,'
                               '     "springLength": 60,'
                               '     "springConstant": 0.16,'
                               '     "nodeDistance": 155,'
                               '     "avoidOverlap": 1'
                               '  },'
                               '"minVelocity": 0.75,'
                               '"solver": "hierarchicalRepulsion"'
                               '},'
                               '"layout" : {'
                               '"clusterThreshold": 150'
                               ' },'
                               '"stabilization": '
                      '{'
                         ' "enabled": true,'
                          '"iterations": 1000,'
                          '"fit": true'
                      '   }'

                               '}')

        options_5_forceAtlas2Based = ('options = {'
                                     '"nodes": '
                                     '{'
                                     '      "font":'
                                     '      {'
                                     '           "size": 25,'
                                     '           "color":"#000000" '
                                     '       },'
                                     '       "margin": 10,'
                                     '       "widthConstraint":'
                                     '       {   '
                                     '           "minimum": 150,'
                                     '           "maximum": 250'
                                     '       }   '
                                     '}, '
                                     '"interaction": {"dragView": true,"hover":true, "selectConnectedEdges": false,"tooltipDelay":500}, '
                                     '"physics": {'
                                     '   "forceAtlas2Based": {'
                                     '   "theta": 1,'
                                     '   "gravitationalConstant": -429,'
                                     '   "centralGravity": 0.055,'
                                     '   "springLength": 205,'
                                     '   "springConstant": 0.56,'
                                     '   "damping": 0.53,'
                                     '   "avoidOverlap": 0.46'
                                     '   },'
                                     '"minVelocity": 0.75,'
                                     '"solver": "forceAtlas2Based"'
                                     '},'
                                     '"layout" : {'
                                     '"clusterThreshold": 150'
                                     ' },'
                                   '"stabilization": '
                      '{'
                         ' "enabled": true,'
                          '"iterations": 1000,'
                          '"fit": true'
                      '   }'

                                     '}')

        # see https://visjs.github.io/vis-network/docs/network/#options => {"configure":{"showButton":true}}
        if visualisation_option == 2:
            print(options_2_spiderweb)
            g.set_options(options_2_spiderweb)
        elif visualisation_option == 3:
            print(options_3_shell)
            g.set_options(options_3_shell) # only formatting the nodes, turns off physics and hierarchy

            asset_ids = [ self.get_corrected_identificator(OTL_asset) for OTL_asset in assets ]
            connected_edge_ids = [(OTL_relation.bronAssetId.identificator, OTL_relation.doelAssetId.identificator) for OTL_relation in relations]


            # Compute shell layout positions
            G = nx.Graph()
            G.add_nodes_from(asset_ids)
            G.add_edges_from(connected_edge_ids)
            pos = nx.shell_layout(G)


            scale = max((500/17) * len(asset_ids), 300)

            # apply the shell graph positions to the pyvis network
            for node_id, node_pos in pos.items():
                node = g.get_node(node_id)
                if node:
                    node["x"] = node_pos[0]*scale
                    node["y"] = node_pos[1]*scale
        elif visualisation_option == 4:
            print(options_4_hierarch_repulsion)
            g.set_options(options_4_hierarch_repulsion)
        elif visualisation_option == 5:
            print(options_5_forceAtlas2Based)
            g.set_options(options_5_forceAtlas2Based)
            
        else:
            print(options_1_hierarchisch)
            g.set_options(options_1_hierarchisch)




        g.write_html(str(html_path), notebook=notebook_mode)
        self.modify_html(Path(html_path), notebook=notebook_mode)
        if not self.notebook_mode and launch_html:
            webbrowser.open(str(html_path))

    def add_object_to_ordering(self, o, relations_per_asset_doel, asset_id):
        typeURI = o.typeURI
        if not typeURI in relations_per_asset_doel:
            relations_per_asset_doel[typeURI] = defaultdict(dict)

        if hasattr(o, "rol"):
            rol = o.rol
        else:
            rol = "None"
        if not rol in relations_per_asset_doel[typeURI]:
            relations_per_asset_doel[typeURI][rol] = defaultdict(
                list)
        relations_per_asset_doel[typeURI][rol][asset_id].append(o)

    @classmethod
    def get_corrected_identificator(cls, otl_object: RelationInteractor):
        identificator = "no_identificator"
        if hasattr(otl_object, "assetId"):
            identificator = str(otl_object.assetId.identificator)
        elif hasattr(otl_object, "agentId"):
            identificator = str(otl_object.agentId.identificator)

        return identificator

    def get_screen_name(cls, otl_object: RelationInteractor) -> Optional[str]:
        if otl_object is None:
            return None
        naam = cls.abbreviate_if_AIM_id(cls.get_corrected_identificator(otl_object))
        if otl_object.typeURI == 'http://purl.org/dc/terms/Agent':
            agent: Agent = otl_object
            # agent will always be external
            external_tranlation = "extern"

            if hasattr(agent, 'naam') and agent.naam:
                naam = " ".join([agent.naam, f"({external_tranlation})"])
            else:
                naam = " ".join([naam, f"({external_tranlation})"])
        else:
            aim_object: AIMObject =  otl_object
            if hasattr(aim_object, 'naam') and aim_object.naam:
                naam = aim_object.naam
            else:
                naam = naam

            if aim_object.assetId.toegekendDoor == "OTL Wizard 2":
                external_tranlation = "external"
                naam = " ".join([naam, f"({external_tranlation})"])

        return naam

    def create_special_nodes_and_relations(self, g, assets, relations, initial_relations_per_asset,
                                           use_bron:bool=True, directed:bool=True,collection_threshold=10):
        assets_with_to_many = []
        assets_count = len(assets)

        single_level_dict = self.recursive_unpack_nested_dict_to_single_level_dict(
            initial_relations_per_asset)

        self.asset_id_to_display_name_dict = {
            self.get_corrected_identificator(asset): self.get_screen_name(asset) for asset in
            assets}

        for asset in assets:
            asset_id = self.get_corrected_identificator(asset)

            if asset_id in single_level_dict.keys():
                # for relations_per_asset in single_level_dict[asset_id]:
                relation_lists_per_asset = single_level_dict[asset_id]

                
                for relations_per_asset in relation_lists_per_asset:
                
                    needs_collection = len(relations_per_asset) >= collection_threshold
                    
                    if needs_collection:
                        assets_with_to_many.append(asset)


                        relatie = deepcopy(relations_per_asset[0])
                        new_node_id = f"special_node_{len(self.special_nodes)}_{self.asset_id_to_display_name_dict[asset_id]}"
                        if directed:
                            if use_bron:
                                list_of_ids = []
                                for rel in relations_per_asset:
                                    display_name =  self.asset_id_to_display_name_dict[rel.bronAssetId.identificator]
                                    list_of_ids.append(display_name)
                                    self.relation_id_to_collection_id[rel.assetId.identificator].append(new_node_id)
                                    self.collection_id_to_list_of_relation_ids[new_node_id].append((rel.assetId.identificator,display_name))

                                self.create_special_node(g, new_node_id=new_node_id,
                                                         list_of_ids=list_of_ids)
                                relatie.bronAssetId.identificator = new_node_id
                                relatie.assetId.identificator = f"special_edge_{len(self.special_edges)}_{relatie.assetId.identificator}"

                                # remove the relations from the original list
                                for relation in relations_per_asset:
                                    relation_copy = deepcopy(relation)
                                    if relation in relations:
                                        relation_copy = deepcopy(relation)
                                        relations.remove(relation)
                                    else:
                                        relation_copy = \
                                        self.collection_relations_id_to_relation_data[
                                            relation.assetId.identificator]
                                    relation_copy.doelAssetId.identificator = new_node_id
                                    self.collection_relations_id_to_relation_data[relation.assetId.identificator] = relation_copy


                            else:
                                list_of_ids = []
                                for rel in relations_per_asset:
                                    display_name = self.asset_id_to_display_name_dict[
                                        rel.doelAssetId.identificator]
                                    list_of_ids.append(display_name)
                                    self.relation_id_to_collection_id[rel.assetId.identificator].append(new_node_id)
                                    self.collection_id_to_list_of_relation_ids[new_node_id].append(
                                        (rel.assetId.identificator, display_name))

                                self.create_special_node(g, new_node_id=new_node_id,
                                                         list_of_ids=list_of_ids)
                                relatie.doelAssetId.identificator = new_node_id
                                relatie.assetId.identificator = f"special_edge_{len(self.special_edges)}_{relatie.assetId.identificator}"

                                # remove the relations from the original list
                                for relation in relations_per_asset:
                                    
                                    if relation in relations:
                                        relation_copy = deepcopy(relation)
                                        relations.remove(relation)
                                    else:
                                        relation_copy = self.collection_relations_id_to_relation_data[
                                            relation.assetId.identificator]
                                 
                                    relation_copy.bronAssetId.identificator = new_node_id
                                    self.collection_relations_id_to_relation_data[
                                        relation.assetId.identificator] = relation_copy
                        else:
                            # for undirected relation detects the bronAssetId or doelAssetId itself
                            list_of_ids = []

                            for rel in relations_per_asset:
                                if rel.doelAssetId.identificator == asset_id:
                                    display_name = self.asset_id_to_display_name_dict[
                                        rel.bronAssetId.identificator]
                                elif rel.bronAssetId.identificator == asset_id:
                                    display_name = self.asset_id_to_display_name_dict[
                                        rel.doelAssetId.identificator]
                                list_of_ids.append(display_name)

                                self.relation_id_to_collection_id[
                                    rel.assetId.identificator].append(new_node_id)
                                self.collection_id_to_list_of_relation_ids[new_node_id].append(
                                    (rel.assetId.identificator, display_name))

                            self.create_special_node(g, new_node_id=new_node_id,
                                                     list_of_ids=list_of_ids)
                            if relatie.doelAssetId.identificator == asset_id:
                                relatie.bronAssetId.identificator = new_node_id
                            elif relatie.bronAssetId.identificator == asset_id:
                                relatie.doelAssetId.identificator = new_node_id
                            
                            
                            relatie.assetId.identificator = f"special_edge_{len(self.special_edges)}_{relatie.assetId.identificator}"

                            # remove the relations from the original list
                            for relation in relations_per_asset:
                                relation_copy = deepcopy(relation)
                                if relation in relations:
                                    relations.remove(relation)
                                else:
                                    relation_copy =  self.collection_relations_id_to_relation_data[
                                    relation.assetId.identificator]


                                if relation_copy.doelAssetId.identificator == asset_id:
                                    relation_copy.doelAssetId.identificator = new_node_id
                                elif relation_copy.bronAssetId.identificator == asset_id:
                                    relation_copy.bronAssetId.identificator = new_node_id
                                
                                self.collection_relations_id_to_relation_data[
                                    relation.assetId.identificator] = relation_copy

                        self.special_nodes.append(g.get_node(new_node_id))

                        asset_ids = (asset_id, new_node_id)
                        self.create_relation_edge(asset_ids, g, relatie)
                        self.special_edges.extend([edge for edge in g.get_edges() if
                                                   edge["id"] == relatie.assetId.identificator])


    def recursive_unpack_nested_dict_to_single_level_dict(self, nested_dicts:dict, single_level_dict =None):
        if not single_level_dict:
            single_level_dict = defaultdict(list)
        for key,value in nested_dicts.items():
            if isinstance(value,list):
                single_level_dict[key].append(value)
            else:
                single_level_dict = self.recursive_unpack_nested_dict_to_single_level_dict(value, single_level_dict)

        return single_level_dict

    def create_nodes(self, g, list_of_objects: [OTLObject]) -> [OTLObject]:
        list_of_objects = self.remove_duplicates_in_iterable_based_on_asset_id(list_of_objects)

        nodes = []
        for index, otl_object in enumerate(list_of_objects):
            screen_name = self.get_screen_name(otl_object=otl_object)

            # if otl_object.typeURI == 'http://purl.org/dc/terms/Agent':
            #     naam = f'{self.abbreviate_if_AIM_id(otl_object.agentId.identificator)[:self.max_screen_name_char_count]}\n<b>{otl_object.__class__.__name__}</b>'
            # else:
            #     naam = f'{self.abbreviate_if_AIM_id(otl_object.assetId.identificator)[:self.max_screen_name_char_count]}\n<b>{otl_object.__class__.__name__}</b>'
            # if hasattr(otl_object, 'naam') and otl_object.naam:
            #     naam = f'{otl_object.naam}\n<b>{otl_object.__class__.__name__}</b>'
            naam = f'{screen_name[:self.max_screen_name_char_count]}\n<b>{otl_object.__class__.__name__}</b>'

            selected_color = self.random_color_if_not_in_dict(otl_object.typeURI)
            color_settings = {
                                  "border": "#000000",
                                  "background":selected_color,
                                  "highlight":
                                  {
                                          "border": "#000000",
                                          "background": "#25bedd"
                                  },
                                  "hover": {
                                        "border": "#000000",
                                        "background": selected_color
                                  }
                            }


            tooltip = self.get_tooltip(otl_object)
            size = 20
            shape = 'box'#'square'
            if otl_object.typeURI.startswith('https://lgc.'):
                shape = 'ellipse'#'diamond'
            elif otl_object.typeURI == 'http://purl.org/dc/terms/Agent':
                shape = 'circle'
                size = 20

            if otl_object.typeURI == 'http://purl.org/dc/terms/Agent':
                node_id = otl_object.agentId.identificator
            else:
                node_id = otl_object.assetId.identificator
            g.add_node(node_id,
                       label=naam,
                       shape=shape,
                       size=size,
                       color=color_settings,
                       font={"multi":True})

            g.get_node(node_id)['title'] = tooltip

            nodes.append(otl_object)
        return nodes

    @classmethod
    def get_all_ids_from_objects(cls, nodes: [OTLObject]) -> [str]:
        for node in nodes:
            if node.typeURI == 'http://purl.org/dc/terms/Agent':
                yield node.agentId.identificator
            else:
                yield node.assetId.identificator

    def create_edges(self, g, list_of_objects: [OTLObject], nodes) -> None:
        asset_ids = list(self.get_all_ids_from_objects(nodes))
        asset_ids.extend(self.collection_id_to_list_of_relation_ids.keys())
        relaties = self.remove_duplicates_in_iterable_based_on_asset_id(list_of_objects)

        for relatie in relaties:
            self.create_relation_edge(asset_ids, g, relatie)

        for collection_relatie in self.collection_relations_id_to_relation_data.values():
            self.create_relation_edge(asset_ids, g, collection_relatie,physics=False,hidden=True)
    
       
    def create_relation_edge(self, asset_ids, g, relatie,physics=True,hidden=False):
        if relatie.bronAssetId.identificator in asset_ids and relatie.doelAssetId.identificator in asset_ids:
            # only display relations between assets that are displayed
            if is_directional_relation(relatie):
                if (
                        relatie.typeURI == 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBetrokkene'
                        and relatie.rol is not None):
                    g.add_edge(id=relatie.assetId.identificator,
                               source=relatie.bronAssetId.identificator,
                               to=relatie.doelAssetId.identificator,
                               color=self.map_relation_to_color(relatie),
                               width=2, arrowStrikethrough=False, label=relatie.rol,
                               smooth={"enabled": False},physics=physics,hidden=hidden)
                else:
                    g.add_edge(id=relatie.assetId.identificator,
                               source=relatie.bronAssetId.identificator,
                               to=relatie.doelAssetId.identificator,
                               color=self.map_relation_to_color(relatie),
                               width=2, arrowStrikethrough=False, smooth={"enabled": False},
                               physics=physics,hidden=hidden)
            else:
                g.add_edge(id=relatie.assetId.identificator,
                           to=relatie.bronAssetId.identificator,
                           source=relatie.doelAssetId.identificator,
                           color=self.map_relation_to_color(relatie),
                           width=2, arrowStrikethrough=False, label='remove_arrow',
                           smooth={"enabled": False},physics=physics,hidden=hidden)

    def map_relation_to_color(self, relatie: OTLObject) -> str:
        return self.relatie_color_dict.get(relatie.typeURI, 'brown')

    def random_color_if_not_in_dict(self, type_uri: str) -> str:
        if type_uri not in self.color_dict.keys():
            if type_uri == 'http://purl.org/dc/terms/Agent':
                random_color = '#FFA500'
            if len(self.color_dict) < len(self.awv_color_list):
                random_color = self.awv_color_list[len(self.color_dict)]
                self.color_dict[type_uri] = random_color
            else:
                random_color = choice(self.list_of_colors)
                while random_color in self.color_dict.values():
                    random_color = choice(self.list_of_colors)
                self.color_dict[type_uri] = random_color

        return self.color_dict[type_uri]

    @classmethod
    def get_tooltip(cls, otl_object: OTLObject) -> str:
        html = (str(otl_object).replace('<', '').replace('>', '').
                replace('\n', '<br/>').replace(' ', '&nbsp;'))
        return f'<htmlTitle>("<div style="font-family: monospace;">{html}</div>")<htmlTitleEnd>'

    
    def modify_html(self, file_path: Path, notebook: bool = False) -> None:
        with open(file_path) as file:
            file_data = file.readlines()

        index_of_function = -1
        index_of_nodes = -1
        index_of_edges = -1
        index_of_screen_height = -1
        index_of_border = -1
        index_of_card_class = -1
        for index, line in enumerate(file_data):
            if index_of_function == -1 and ('// This method is responsible for drawing the graph, '
                                            'returns the drawn network') in line:
                index_of_function = index
            elif index_of_nodes == -1 and 'nodes = new vis.DataSet' in line:
                index_of_nodes = index
            elif index_of_edges == -1 and 'edges = new vis.DataSet' in line:
                index_of_edges = index
            elif index_of_screen_height == -1 and 'height: 600px;' in line:
                index_of_screen_height = index
            elif index_of_border == -1 and 'border: 1px solid lightgray;' in line:
                index_of_border = index
            elif index_of_card_class == -1 and 'class="card"' in line:
                index_of_card_class = index

        nodes_line = file_data.pop(index_of_nodes)
        nodes_line = nodes_line.replace('"\\u003chtmlTitle\\u003e(\\\"', 'htmlTitle("'). \
                replace('\\\")\\u003chtmlTitleEnd\\u003e"', '")').replace('\\u003c', '<').replace('\\u003e', '>')
        file_data.insert(index_of_nodes, nodes_line)

        self.modify_edges_in_html(file_data=file_data, index_of_edges=index_of_edges)
        #insert handler that activates when DOMcontent is loaded
        file_data.insert(index_of_function - 5,
                         'document.addEventListener("DOMContentLoaded", (event) => {\n')
        file_data.insert(index_of_function - 4,
                         'document.getElementById("mynetwork").style.display="flex";\n')
        file_data.insert(index_of_function - 3,
                        '});\n')
        #add html title?
        file_data.insert(index_of_function - 2, '              // text to html element\n')
        file_data.insert(index_of_function - 1, '              function htmlTitle(html) {' + '\n')
        file_data.insert(index_of_function, '                const container = document.createElement("div");' + '\n')
        file_data.insert(index_of_function + 1, '                container.innerHTML = html;' + '\n')
        file_data.insert(index_of_function + 2, '                return container;' + '\n')
        file_data.insert(index_of_function + 3, '              }' + '\n')

        # insert handler that activates when DOMcontent is loaded
        # file_data.insert(index_of_function + 4,
        #                  'document.addEventListener("DOMContentLoaded", (event) => {\n')
        # file_data.insert(index_of_function + 5,
        #                  'document.getElementById("mynetwork").style.display="flex";\n')
        # file_data.insert(index_of_function + 6,
        #                  '});\n')
        add_data = ['var nodeSelected = false;',
                    'var relationIdToSubEdges = new Map();',
                    'var relationIdToTotalSubEdgeCount = new Map();',
                    'var relationIdToJointNodes = new Map();',
                    'var SubEdgesToOriginalRelationId = new Map();',
                    'var edgeJointNodesIdToConnectionDataDict = new Map(); ',
                    'var newWidth = 0;',
                    'var newHeight = 0;',
                    'var ctrlSelectedNodesList = []; //to store all the nodeIds that have been clicked while holding down ctrl',
                    'var lastCtrlSelectedNode = null;',
                    'var currentlyHoveredNode = null;',
                    'var noTooltips = false;',
                    f'var collection_id_to_list_of_relation_ids = {json.dumps(self.collection_id_to_list_of_relation_ids)};',
                    'document.addEventListener("DOMContentLoaded", (event) => ',
                    '{',
                    # '   network.on("beforeDrawing",  function(ctx) ',
                    # '   {',
                    # '       //fill the canvas with a white background before drawing',
                    # '       // save current translate/zoom',
                    # '       ctx.save();',
                    # '       // reset transform to identity',
                    # '       ctx.setTransform(1, 0, 0, 1, 0, 0);',
                    # '       // fill background with solid white',
                    # "       ctx.fillStyle = '#ffffff';",
                    # '       ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height)',
                    # '       // restore old transform',
                    # '       ctx.restore();',
                    # # '       console.log("before drawing: " + ctx.canvas.clientWidth + ", " + ctx.canvas.clientHeight);'
                    # '   })'
                    '   ',
                    "   network.on('selectEdge', function(params) ",
                    "   {",
                    "       if (nodeSelected)",
                    "       {",
                    "           nodeSelected = false;" ,
                    "           return",
                    "       }",
                    "       if (params.edges.length > 0) ",
                    "       {",
                    # "           console.log('Edge clicked:', params.edges, 'clicked at DOM', params.pointer.DOM, 'and canvas',params.pointer.canvas);",
                    "           var clickedEdge = network.body.data.edges._data.get(params.edges[0]);",
                    "           addEdgeJointNode(params.pointer.canvas.x, params.pointer.canvas.y,clickedEdge);",
                    "           network.selectEdges([]);",
                    # "       sendCurrentCombinedDataToPython()",
                    "       }",
                    "   });",
                    # "   network.on('click', function(params) ",
                    # "   {",
                    # "       console.log(params);",
                    # "   });",
                    "   network.on('selectNode', function(params) ",
                    "   {",
                    "       if (params.nodes.length > 0) ",
                    "       {",
                    "           if (params.event.srcEvent.ctrlKey)",
                    "           {",
                    "               lastCtrlSelectedNode = params.nodes[0]",
                    "               ctrlSelectedNodesList.push(lastCtrlSelectedNode);",
                    "               network.selectNodes(ctrlSelectedNodesList,false);",
                    "           }",
                    "           else",
                    "               ctrlSelectedNodesList = params.nodes;",
                    "           ",
                    # "           console.log('node clicked:', params);",
                    "           nodeSelected = true //just here to make sure the event for edge selection is not triggered",
                    "       }",
                    "   });",
                    "   network.on('showPopup', function(params) ",
                    "   {",
                    "       if (noTooltips)",
                    "       {",
                    "           return"
                    "       }",
                    "   });",
                    "   network.on('select', function(params) ",
                    "   {",
                    # "       console.log('selection changed clicked:', params.nodes,params.edges);",
                    "       currentlyClickedNode = network.getNodeAt(params.pointer.DOM);",
                    # "       console.log('currentlyClickedNode:', currentlyClickedNode);",
                    "       if(currentlyClickedNode)",
                    "       {" ,
                    "           if(lastCtrlSelectedNode != currentlyClickedNode &&",
                    "               params.event.srcEvent.ctrlKey && ",
                    "               ctrlSelectedNodesList.includes(currentlyClickedNode)) ",
                    "           {",
                    "               const index = ctrlSelectedNodesList.indexOf(currentlyClickedNode);",
                    "               if (index > -1) // only splice array when item is found",
                    "               { ",
                    "                   ctrlSelectedNodesList.splice(index, 1); // 2nd parameter means remove one item only",
                    "                   network.selectNodes(ctrlSelectedNodesList,false);",
                    "               }",
                    "           }",
                    "       }",
                    "       else if(!params.event.srcEvent.ctrlKey)",
                    "       {",
                    "           ctrlSelectedNodesList = [];",
                    "       }",
                    "       lastCtrlSelectedNode = null;" ,
                    # "       if(params.edges.length == 1)",
                    # "       {",
                    # "           var clickedEdge = network.body.data.edges._data.get(params.edges[0]);",
                    # "           addEdgeJointNode(params.pointer.canvas.x, params.pointer.canvas.y, clickedEdge);",
                    # "           network.selectEdges([]);",
                    # # "           sendCurrentCombinedDataToPython()",
                    # "       }",
                    "   });",
                    "   network.on('hoverNode', function(params) ",
                    "   {",
                    "       if (params.node.includes('special_node') && (params.node in collection_id_to_list_of_relation_ids))",
                    "       {",
                    '           // hide all relations in de collection when not hovering on collection',
                    '          var relations_in_collection_list = collection_id_to_list_of_relation_ids[params.node]',
                    '          var updateData = []',
                    '          for (const index in relations_in_collection_list) ',
                    '           {',
                    '               var relation_id = relations_in_collection_list[index][0]',
                    '               console.log(relation_id)',
                    "               updateData.push({'id': relation_id, 'hidden': false})",
                    '           }',
                    "           applyUpdateEdgeInNetwork(updateData, notify_python=false);",
                    "       }",
                    "       if (params.node.includes('edgeJoint'))",
                    "       {",
                    "           applyUpdateNodeInNetwork({'id': params.node,'opacity': 1}, notify_python=false);",
                    "           currentlyHoveredNode = params.node //used in dragMultiSelect.js",
                    "       }",
                    "       //don't show tooltip if your pressing ctrl or right-mouse (buttons == 2)",
                    "       noTooltips = params.event.ctrlKey || params.event.buttons == 2",
                    "   });",
                    "   network.on('blurNode', function(params) ",
                    "   {",
                    "       "
                    "       if (params.node.includes('special_node') && (params.node in collection_id_to_list_of_relation_ids))",
                    "       {",
                    '           // hide all relations in de collection when not hovering on collection',
                    '          var relations_in_collection_list = collection_id_to_list_of_relation_ids[params.node]',
                    '          var updateData = []',
                    '          for (const index in relations_in_collection_list) ' ,
                    '           {',
                    '               var relation_id = relations_in_collection_list[index][0]',
                    '               console.log(relation_id)',
                    "               updateData.push({'id': relation_id, 'hidden': true})",
                    '           }',
                    "           applyUpdateEdgeInNetwork(updateData, notify_python=false);",
                    "       }",
                    "       if (params.node.includes('edgeJoint') && network.body.data.nodes._data.has(params.node))",
                    "       {",
                    "           applyUpdateNodeInNetwork({'id': params.node,'opacity': 0}, notify_python=false);",
                    "           currentlyHoveredNode = null //used in dragMultiSelect.js",
                    "       }",
                    "       noTooltips = params.event.ctrlKey || params.event.buttons == 2",
                    "   });",
                    "   network.on('dragEnd', function(params) ",
                    "   {",
                    # "      console.log('dragEnd:', params);",
                    "      if (params.nodes.length > 0)",
                    "      {",
                    "           var draggedNodeId = params.nodes[0]; ",
                    "           if (draggedNodeId.includes('edgeJoint'))",
                    "           {",
                    "               var newPos = network.getPosition(draggedNodeId)",
                    "               var draggedNode = network.body.data.nodes._data.get(draggedNodeId);",
                    "               applyUpdateNodeInNetwork({'id': draggedNodeId,'x':  newPos.x,'y': newPos.y});",
                    "           }",
                    "           else",
                    "               sendNetworkChangedNotificationToPython();",
                    "      }",
                    "   });",
                    '});',
                    "function addEdgeJointNode(x,y,clickedEdge)",
                    "{",
                    # "   console.log(clickedEdge);",
                    '   var edgeId = clickedEdge["id"];',
                    # "   var edgeJointNodeNbrPerEdge = network.body.data.nodes.length;",
                    "   var edgeJointNodeNbrPerEdge = 0;",
                    "   if ( relationIdToJointNodes.has(edgeId))",
                    "       edgeJointNodeNbrPerEdge =  relationIdToJointNodes.get(edgeId).length;",
                    "   else",
                    # "   if (!relationIdToJointNodes.has(edgeId))",
                    "       relationIdToJointNodes.set(edgeId, []);",
                    '   var newEdgeJointNodeId = "edgeJoint_" + edgeJointNodeNbrPerEdge + "_" + edgeId;',
                    "   relationIdToJointNodes.get(edgeId).push(newEdgeJointNodeId);",
                    "   edgeJointNodesIdToConnectionDataDict.set(newEdgeJointNodeId, {});",
                    '   var selected_color = "#" + clickedEdge["color"]',
                    "   var color_settings = {",
                    '              "border": "#000000",',
                    '              "background":selected_color,',
                    '              "highlight":',
                    '              {',
                    '                      "border": "#000000",',
                    '                      "background": "#25bedd"',
                    '              },',
                    '              "hover": {',
                    '                    "border": "#000000",',
                    '                    "background": selected_color',
                    '              }',
                    '        }',
                    " ",
                    "   applyAddNodesToNetwork([{"
                    "       'x': x,"
                    "       'y': y,"
                    '       "color": color_settings,'
                    '       "id": newEdgeJointNodeId,'
                    '       "shape": "dot",'
                    '       "size": 10'
                    '   }])',
                    # "   console.log('newEdgeJointNodeId: ' + newEdgeJointNodeId);",
                    "   ",
                    "   addSubEdgesToEdgeJointNode(clickedEdge, newEdgeJointNodeId)",
                    "   ",
                    "   "
                    "}",
                    "function addSubEdgesToEdgeJointNode(clickedEdge,newEdgeJointNodeId)",
                    "{",
                    # "   console.log(clickedEdge);",
                    '   var edgeId = clickedEdge["id"];',
                    "   var subEdge1Nbr = 0;",
                    # "   var subEdge1Nbr = network.body.data.edges.length;",
                    "   ",
                    "   var originalEdgeId = edgeId",
                    "   if ( SubEdgesToOriginalRelationId.has(edgeId))",
                    "   {",
                    "       originalEdgeId =  SubEdgesToOriginalRelationId.get(edgeId);//if the clicked edge was a subedge get the original relationId",
                    "       SubEdgesToOriginalRelationId.delete(edgeId);",
                    "       ",
                    "       subEdge1Nbr =  relationIdToTotalSubEdgeCount.get(originalEdgeId);",
                    "       var subEdges = relationIdToSubEdges.get(originalEdgeId);",
                    "       var removeSubEdgeIndex = subEdges.indexOf(edgeId);",
                    "       subEdges.splice(removeSubEdgeIndex,1);",
                    "   }",
                    "   else",
                    "   {",
                    "       if ( relationIdToSubEdges.has(originalEdgeId))",
                    "           subEdge1Nbr =  relationIdToSubEdges.get(originalEdgeId).length;",
                    "       else",
                    "       {"
                    "           relationIdToTotalSubEdgeCount.set(originalEdgeId, 0);",
                    "           relationIdToSubEdges.set(originalEdgeId, []);",
                    "       }"
                    "   }",
                    # "   var subEdge2Nbr = subEdge1Nbr + 1;",
                    "   ",
                    "   var newUniqueId = crypto.randomUUID()",
                    '   var newSubEdge1Id = "subEdge_" + subEdge1Nbr + "_" + newUniqueId;',
                    '   var newSubEdge2Id = "subEdge_sec_" + subEdge1Nbr + "_" + newUniqueId;',
                    "   relationIdToSubEdges.get(originalEdgeId).push(newSubEdge1Id);",
                    "   relationIdToSubEdges.get(originalEdgeId).push(newSubEdge2Id);",
                    "   relationIdToTotalSubEdgeCount.set(originalEdgeId, relationIdToTotalSubEdgeCount.get(originalEdgeId)+1);",
                    "   SubEdgesToOriginalRelationId.set(newSubEdge1Id, originalEdgeId);",
                    "   SubEdgesToOriginalRelationId.set(newSubEdge2Id,originalEdgeId);",

                    "   newSubEdge1Data = JSON.parse(JSON.stringify(clickedEdge));",
                    "   newSubEdge2Data = JSON.parse(JSON.stringify(clickedEdge));",
                    "   ",
                    "   newSubEdge1Data.id = newSubEdge1Id;",
                    "   newSubEdge1Data.from = newEdgeJointNodeId;",
                    "   ",
                    "   newSubEdge2Data.id = newSubEdge2Id",
                    "   newSubEdge2Data.to = newEdgeJointNodeId;",
                    "   newSubEdge2Data.arrows = null;",
                    "   ",
                    # "   console.log('newSubEdge1Data.id: ' + newSubEdge1Data.id);",
                    # "   console.log('newSubEdge2Data.id: ' + newSubEdge2Data.id);",
                    "   applyAddEdgesToNetwork([newSubEdge1Data,newSubEdge2Data])",
                    "   applyRemoveEdgesFromNetwork([edgeId])",
                    "   ",
                    "   //save the connections to the new joint node for later removal",
                    "   var connection_data = { ",
                    "       'originalEdgeId': originalEdgeId,",
                    "       'previousEdgeId': edgeId,",
                    "       'newSubEdge1Id': newSubEdge1Id,",
                    "       'newSubEdge2Id': newSubEdge2Id,",
                    "       'newSubEdge1Data.to': newSubEdge1Data.to,",
                    "       'newSubEdge2Data.from': newSubEdge2Data.from,",
                    "       }",
                    "   edgeJointNodesIdToConnectionDataDict.set(newEdgeJointNodeId, connection_data);",
                    '   //edit supporting data of the to and from nodes so they have the correct',
                    '   //to and from themselves',
                    '   updateNeighbouringEdgeJointNode(newSubEdge1Data.to, newSubEdge2Data.from, newEdgeJointNodeId)',
                    '   updateNeighbouringEdgeJointNode(newSubEdge2Data.from, newSubEdge1Data.to, newEdgeJointNodeId)',
                    '   updateConnectingEdgeOnNeighbouringEdgeJointNode(newSubEdge1Data.to,edgeId,newSubEdge1Id)',
                    '   updateConnectingEdgeOnNeighbouringEdgeJointNode(newSubEdge2Data.from,edgeId,newSubEdge2Id)',
                    # '   console.log("add edge jointnode")',
                #     'edgeJointNodesIdToConnectionDataDict.forEach((data,key) =>',
                # '      {',
                # '         console.log(key +": " + JSON.stringify(data))',
                # '      })',
                # '   console.log(" network.body.data.edges:\\n ")',
                # 'network.body.data.edges._data.forEach((data,key) =>',
                # '      {',
                # '         console.log(key +": " + JSON.stringify(data))',
                # '      })',
                    "   ",
                    "}",
                    ]
        # the function that communicates changes in the network to the python backend
        add_data.extend(self.create_sendNetworkChangedNotificationToPython_js_function())
        # interfaces that are intended as the only ones allowed to edit the network data
        # Because they will always notify the python backend of the change (see js function above)
        add_data.extend(self.create_applyRemoveEdgesFromNetwork_js_function())
        add_data.extend(self.create_applyRemoveNodesFromNetwork_js_function())
        add_data.extend(self.create_applyAddNodesToNetwork_js_function())
        add_data.extend(self.create_applyAddEdgesToNetwork_js_function())
        add_data.extend(self.create_applyUpdateEdgeInNetwork_js_function())
        add_data.extend(self.create_applyUpdateNodeInNetwork_js_function())
        add_data.extend(self.create_updateNeighbouringEdgeJointNode_js_function())
        add_data.extend(self.create_updateConnectingEdgeOnNeighbouringEdgeJointNode_js_function())
        
        self.replace_and_add_lines(file_data,index_of_function + 4,"","",add_data)


        if index_of_screen_height != -1:
            screen_height_line = file_data.pop(index_of_screen_height)
            if notebook:
                screen_height_line = screen_height_line.replace('height: 600px;', 'height: 800px;')
            else:        
                screen_height_line = screen_height_line.replace('height: 600px;', 'height: auto;')
            file_data.insert(index_of_screen_height, screen_height_line)

        if index_of_border != -1:
            border_line = file_data.pop(index_of_border)
            border_line = border_line.replace('border: 1px solid lightgray;', 'border: 0px solid lightgray;')
            file_data.insert(index_of_border, border_line)

        if index_of_card_class != -1 and not notebook:
            card_class_line = file_data.pop(index_of_card_class)
            card_class_line = card_class_line.replace('class="card"', ' ')
            file_data.insert(index_of_card_class, card_class_line)

        with open(file_path, 'w') as file:
            for line in file_data:
                file.write(line)

    @classmethod
    def create_sendNetworkChangedNotificationToPython_js_function(cls):
        return ['function sendNetworkChangedNotificationToPython()',
                "{",
                "   //function that uses the QWebChannel to notify the python application that the network has changed",
                # "   console.log('Network changed through correct interface'); ",
                "   if (window.backend)",
                "   {",
                "       window.backend.receive_network_changed_notification();",
                # "       console.log('called window.backend.receive_network_changed_notification()'); ",
                "   }"
                "   else",
                "   {"
                '       console.log("sendNetworkChangedNotificationToPython: QWebChannel is not initialized yet.");',
                # '       alert("DataVisualisationScreen: QWebChannel is not initialized");',
                "   }",

                "}"]

    @classmethod
    def create_applyRemoveEdgesFromNetwork_js_function(cls):
        return ['function applyRemoveEdgesFromNetwork(edgeIdList, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   network.body.data.edges.remove(edgeIdList);',
                '   ',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_applyRemoveNodesFromNetwork_js_function(cls):
        return ['function applyRemoveNodesFromNetwork(nodeIdList, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   network.body.data.nodes.remove(nodeIdList);',
                '   ',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_applyAddNodesToNetwork_js_function(cls):
        return ['function applyAddNodesToNetwork(nodeCreationDataList, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   network.body.data.nodes.add(nodeCreationDataList);',
                '   ',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_applyAddEdgesToNetwork_js_function(cls):
        return ['function applyAddEdgesToNetwork(edgeCreationDataList, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   network.body.data.edges.add(edgeCreationDataList);',
                '   ',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_applyUpdateEdgeInNetwork_js_function(cls):
        return ['function applyUpdateEdgeInNetwork(changedEdgeData, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   network.body.data.edges.updateOnly(changedEdgeData);',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_applyUpdateNodeInNetwork_js_function(cls):
        return ['function applyUpdateNodeInNetwork(changedNodeData, notify_python=true)',
                '{',
                '   //This is the only function that should call the following function',
                '   //https://stackoverflow.com/questions/32765015/vis-js-modify-node-properties-on-click',
                '   network.body.data.nodes.updateOnly(changedNodeData);',
                '   ',
                '   if(notify_python)',
                '       sendNetworkChangedNotificationToPython();',
                '}']

    @classmethod
    def create_updateNeighbouringEdgeJointNode_js_function(cls):
        return ['function updateNeighbouringEdgeJointNode(nodeIdToUpdate, removedNodeId, newNeighbourNodeId)',
                '{',
                '       //nodeIdToUpdate needs to be an edgeJointNode',
                '       if(!(nodeIdToUpdate.includes("edgeJoint") && edgeJointNodesIdToConnectionDataDict.has(nodeIdToUpdate)))',
                '           return;'
                '       ',
                '       nodeToUpdateConnectionData = edgeJointNodesIdToConnectionDataDict.get(nodeIdToUpdate)',
                '       if(nodeToUpdateConnectionData["newSubEdge1Data.to"] == removedNodeId)',
                '           nodeToUpdateConnectionData["newSubEdge1Data.to"] = newNeighbourNodeId;',
                '       else if(nodeToUpdateConnectionData["newSubEdge2Data.from"] = newNeighbourNodeId)',
                '           nodeToUpdateConnectionData["newSubEdge2Data.from"] = newNeighbourNodeId;',
                '}']

    @classmethod
    def create_updateConnectingEdgeOnNeighbouringEdgeJointNode_js_function(cls):
        return [
            'function updateConnectingEdgeOnNeighbouringEdgeJointNode(nodeIdToUpdate, removedEdgeId, newEdgeId)',
            '{',
            '       //nodeIdToUpdate needs to be an edgeJointNode',
            '       if(!(nodeIdToUpdate.includes("edgeJoint") && edgeJointNodesIdToConnectionDataDict.has(nodeIdToUpdate)))',
            '           return;'
            '       ',
            '       nodeToUpdateConnectionData = edgeJointNodesIdToConnectionDataDict.get(nodeIdToUpdate)',
            '       if(nodeToUpdateConnectionData["newSubEdge1Id"] == removedEdgeId)',
            '           nodeToUpdateConnectionData["newSubEdge1Id"] = newEdgeId;',
            '       else if(nodeToUpdateConnectionData["newSubEdge2Id"] = removedEdgeId)',
            '           nodeToUpdateConnectionData["newSubEdge2Id"] = newEdgeId;',
            '}']

    @classmethod
    def modify_edges_in_html(cls, file_data, index_of_edges):
        if index_of_edges == -1:
            return
        edges_line = file_data.pop(index_of_edges)
        edges_line = edges_line.replace('edges = new vis.DataSet(','').replace(');','')
        edge_dict_list = json.loads(edges_line)
        for edge_dict in edge_dict_list:
            if edge_dict.get('label') == 'remove_arrow':
                edge_dict['arrows'] = None
                del edge_dict['label']
        edges_line = f'edges = new vis.DataSet({json.dumps(edge_dict_list)});'
        file_data.insert(index_of_edges, edges_line)

    @classmethod
    def abbreviate_if_AIM_id(cls,id):
        return id.split("-")[0] + "-..." if OTLObjectHelper.is_aim_id(id) else id

    @classmethod
    def create_special_node(cls,g,new_node_id, list_of_ids:list):
        asset_count = len(list_of_ids)
        naam =f"<i><b>Collectie({asset_count})</b></i>"
        tooltip = f"Collectie({asset_count}):\n"
        for index,identificator in enumerate(list_of_ids):
            tooltip += f'{(index+1)}: {identificator[:cls.max_screen_name_char_count]}\n'


        selected_color = "#CCCCCC"

        color_settings = {
            "border": "#000000",
            "background": selected_color,
            "highlight":
                {
                    "border": "#000000",
                    "background": "#25bedd"
                },
            "hover": {
                "border": "#000000",
                "background": selected_color
            }
        }


        size = 20
        shape = 'database'  # 'diamond'

        node_id = new_node_id
        g.add_node(node_id,
                   label=naam,
                   shape=shape,
                   size=size,
                   color=color_settings,
                   font={"multi":True})
        g.get_node(node_id)['title'] = tooltip


    def create_edge_inject_arguments(self, relatie):

        edge_inject_arguments ={"id" : relatie.assetId.identificator,
                    "from_id": relatie.bronAssetId.identificator,
                    "to_id": relatie.doelAssetId.identificator,
                    "color": self.map_relation_to_color(relatie)}

        if is_directional_relation(relatie):
            edge_inject_arguments["arrow"] = "to"
            if (relatie.typeURI == 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBetrokkene'
                and relatie.rol is not None):
                edge_inject_arguments["label"] = relatie.rol

        return edge_inject_arguments

    @classmethod
    def replace_and_add_lines(cls,file_data, replace_index, start_line_to_replace: str,
                              start_replacement: str, list_of_followup_lines: list[str]):
        file_data[replace_index] = file_data[replace_index].replace(start_line_to_replace,
                                                                    start_replacement)
        for i, followup_line in enumerate(list_of_followup_lines):
            file_data.insert(replace_index + i, followup_line + "\n")
