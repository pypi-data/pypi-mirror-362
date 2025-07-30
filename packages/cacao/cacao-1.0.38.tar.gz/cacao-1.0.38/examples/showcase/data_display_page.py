"""
Data Display page for the components showcase.
Demonstrates data display components like tables, lists, cards, etc.
"""

class DataDisplayPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Data Display Components",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    # Table
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Table",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "table",
                                    "props": {
                                        "columns": [
                                            {"title": "Name", "dataIndex": "name", "key": "name"},
                                            {"title": "Age", "dataIndex": "age", "key": "age"},
                                            {"title": "Address", "dataIndex": "address", "key": "address"}
                                        ],
                                        "dataSource": [
                                            {"key": "1", "name": "John Brown", "age": 32, "address": "New York No. 1 Lake Park"},
                                            {"key": "2", "name": "Jim Green", "age": 42, "address": "London No. 1 Lake Park"},
                                            {"key": "3", "name": "Joe Black", "age": 32, "address": "Sydney No. 1 Lake Park"}
                                        ],
                                        "pagination": {"pageSize": 10, "current": 1}
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Tree Viewer Test
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Tree Viewer",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "tree_viewer",
                                    "props": {
                                        "id": "myTree",
                                        "data": {
                                            "glossary": {
                                                "title": "example glossary",
                                                "GlossDiv": {
                                                    "title": "S",
                                                    "GlossList": {
                                                        "GlossEntry": {
                                                            "ID": "SGML",
                                                            "SortAs": "SGML",
                                                            "GlossTerm": "Standard Generalized Markup Language",
                                                            "Acronym": "SGML",
                                                            "Abbrev": "ISO 8879:1986",
                                                            "GlossDef": {
                                                                "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                                                "GlossSeeAlso": ["GML", "XML"]
                                                            },
                                                            "GlossSee": "markup"
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "expand_all": False,
                                        "theme": "light",
                                        "on_node_click": "tree:nodeClick"
                                    }
                                }
                            ]
                        }
                    },
                    # List
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "List",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "list",
                                    "props": {
                                        "items": [
                                            {"title": "Item 1", "description": "Description for item 1"},
                                            {"title": "Item 2", "description": "Description for item 2"},
                                            {"title": "Item 3", "description": "Description for item 3"}
                                        ],
                                        "bordered": True,
                                        "style": {
                                            "width": "100%"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Descriptions
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Descriptions",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "descriptions",
                                    "props": {
                                        "title": "User Information",
                                        "items": [
                                            {"label": "Name", "content": "John Doe"},
                                            {"label": "Email", "content": "john.doe@example.com"},
                                            {"label": "Phone", "content": "(123) 456-7890"},
                                            {"label": "Address", "content": "123 Main St, Anytown, USA"}
                                        ],
                                        "bordered": True,
                                        "column": 2
                                    }
                                }
                            ]
                        }
                    },
                    # Card, Image, Badge, Avatar, Tag
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "Media Components",
                                        "style": {"marginBottom": "15px"}
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "grid",
                                            "gridTemplateColumns": "repeat(2, 1fr)",
                                            "gap": "20px",
                                            "marginBottom": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "card",
                                                "props": {
                                                    "title": "Card Title",
                                                    "children": "This is the content of the card. Cards can contain any content.",
                                                    "bordered": True,
                                                    "style": {
                                                        "width": "100%"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "card",
                                                "props": {
                                                    "title": "Card with Badge",
                                                    "children": {
                                                        "type": "badge",
                                                        "props": {
                                                            "count": 5,
                                                            "children": {
                                                                "type": "div",
                                                                "props": {
                                                                    "content": "Notifications",
                                                                    "style": {
                                                                        "padding": "20px",
                                                                        "backgroundColor": "#FFFFFF",
                                                                        "border": "1px solid #EEEEEE",
                                                                        "borderRadius": "4px"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "bordered": True,
                                                    "style": {
                                                        "width": "100%"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "h4",
                                                "props": {
                                                    "content": "Avatar & Tags",
                                                    "style": {"marginBottom": "10px"}
                                                }
                                            },
                                            {
                                                "type": "div",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "10px",
                                                        "marginBottom": "15px"
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "avatar",
                                                            "props": {
                                                                "src": "https://via.placeholder.com/40",
                                                                "shape": "circle",
                                                                "size": "large"
                                                            }
                                                        },
                                                        {
                                                            "type": "div",
                                                            "props": {
                                                                "children": [
                                                                    {
                                                                        "type": "p",
                                                                        "props": {
                                                                            "content": "John Doe",
                                                                            "style": {
                                                                                "margin": "0",
                                                                                "fontWeight": "bold"
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "type": "div",
                                                                        "props": {
                                                                            "style": {
                                                                                "display": "flex",
                                                                                "gap": "5px",
                                                                                "marginTop": "5px"
                                                                            },
                                                                            "children": [
                                                                                {
                                                                                    "type": "tag",
                                                                                    "props": {
                                                                                        "content": "Developer",
                                                                                        "color": "blue"
                                                                                    }
                                                                                },
                                                                                {
                                                                                    "type": "tag",
                                                                                    "props": {
                                                                                        "content": "Designer",
                                                                                        "color": "green"
                                                                                    }
                                                                                }
                                                                            ]
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "children": [
                                            {
                                                "type": "h4",
                                                "props": {
                                                    "content": "Timeline",
                                                    "style": {"marginBottom": "10px"}
                                                }
                                            },
                                            {
                                                "type": "timeline",
                                                "props": {
                                                    "items": [
                                                        {"label": "2015", "content": "Created"},
                                                        {"label": "2020", "content": "Updated"},
                                                        {"label": "2025", "content": "Completed"}
                                                    ],
                                                    "mode": "left"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }