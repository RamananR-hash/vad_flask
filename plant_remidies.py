def remedies(disease):
    print(disease)
    remedies_dict = {
    'Bacterial_spot': [
        'Apply copper-based fungicides preventively.',
        'Rotate crops to reduce pathogen buildup.',
        'Prune affected plant parts to minimize spread.',
        'Ensure proper plant spacing for air circulation.',
        'Use disease-resistant tomato varieties when available.'
    ],
    'Early_blight': [
        'Apply fungicides containing copper or chlorothalonil.',
        'Mulch around plants to reduce soil splashing.',
        'Water at the base of plants to minimize leaf wetness.',
        'Rotate crops to prevent pathogen buildup.',
        'Remove and destroy infected plant material.'
    ],
    'Healthy': [
        'Maintain proper irrigation and nutrient levels.',
        'Monitor plants regularly for signs of diseases.',
        'Promote overall plant health through proper care.'
    ],
    'Late_blight': [
        'Apply fungicides containing chlorothalonil or mancozeb.',
        'Provide good air circulation by spacing plants.',
        'Avoid overhead watering to minimize leaf wetness.',
        'Remove and destroy infected plant material promptly.',
        'Choose resistant tomato varieties if available.'
    ],
    'Leaf_mold': [
        'Use fungicides containing copper or mancozeb.',
        'Provide proper plant spacing for air circulation.',
        'Water at the base of plants to avoid wetting leaves.',
        'Remove and destroy infected plant material.',
        'Apply preventive sprays during humid conditions.'
    ],
    'Septoria_Leaf_spot': [
        'Apply fungicides containing copper or chlorothalonil.',
        'Water at the base of plants to keep foliage dry.',
        'Remove infected leaves to reduce disease spread.',
        'Rotate crops to prevent pathogen buildup.',
        'Consider resistant tomato varieties if available.'
    ],
    'Spider_mites_Two_spotted_Spider_mite': [
        'Use insecticidal soaps or neem oil to control mites.',
        'Introduce natural predators like predatory mites.',
        'Maintain proper humidity levels to deter mite infestations.',
        'Spray plants with a strong stream of water to dislodge mites.',
        'Avoid over-fertilization, which can attract mites.'
    ],
    'Target_Spot': [
        'Apply fungicides containing chlorothalonil or mancozeb.',
        'Remove and destroy infected plant material.',
        'Provide proper plant spacing for air circulation.',
        'Avoid overhead irrigation to minimize leaf wetness.',
        'Rotate crops to prevent disease buildup.'
    ],
    'Tomato_Mosaic_virus': [
        'Plant virus-resistant tomato varieties.',
        'Control aphid populations, which can transmit the virus.',
        'Remove and destroy infected plants to prevent spread.',
        'Practice good hygiene to avoid virus transmission.',
        'Avoid planting tomatoes near infected crops.'
    ],
    'Tomato_Yellow_Leaf_Curl_Virus': [
        'Use resistant tomato varieties if available.',
        'Control whitefly populations, which transmit the virus.',
        'Remove and destroy infected plants promptly.',
        'Apply reflective mulches to deter whiteflies.',
        'Avoid planting tomatoes near infected crops.'
    ]
}
    print("Function Called")
    d=disease.split('\n')[0]
    return remedies_dict[d]
