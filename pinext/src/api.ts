import { getExtensionVersion } from './utils'

const API_HOST = 'https://pinext.streamlit.app'

export interface PromotionResponse {
  url: string
  title?: string
  text?: string
  image?: { url: string; size?: number }
  footer?: { text: string; url: string }
  label?: { text: string; url: string }
}

export async function fetchPromotion(): Promise<PromotionResponse | null> {
  return fetch(`${API_HOST}/api/p`, {
    headers: {
      'x-version': getExtensionVersion(),
    },
  }).then((r) => r.json())
}

export async function fetchExtensionConfigs(): Promise<{
  AI21_model_names: string[]
}> {
  return fetch(`${API_HOST}/api/config`, {
    headers: {
      'x-version': getExtensionVersion(),
    },
  }).then((r) => r.json())
}
