import Browser from 'webextension-polyfill'
import { getProviderConfigs, ProviderType } from '../config'
import { J2Provider, getAI21AccessToken, sendMessageFeedback } from './providers/J2'
import { AI21Provider } from './providers/ai21'
import { Provider } from './types'

async function generateAnswers(port: Browser.Runtime.Port, question: string) {
  const providerConfigs = await getProviderConfigs()

  let provider: Provider
  if (providerConfigs.provider === ProviderType.J2ULTRA) {
    const { apiKey, model } = providerConfigs.configs[ProviderType.J2ULTRA]!
    provider = new J2Provider(apiKey, model)
  } 
  else if (providerConfigs.provider === ProviderType.J2MID) {
    const { apiKey, model } = providerConfigs.configs[ProviderType.J2MID]!
    provider = new J2Provider(apiKey, model)
  } 
  else if (providerConfigs.provider === ProviderType.J2LIGHT) {
	  const { apiKey, model } = providerConfigs.configs[ProviderType.J2LIGHT]!
	  provider = new J2Provider(apiKey, model)
  }
  else {
    throw new Error(`Unknown provider ${providerConfigs.provider}`)
  }

  const controller = new AbortController()
  port.onDisconnect.addListener(() => {
    controller.abort()
    cleanup?.()
  })

  const { cleanup } = await provider.generateAnswer({
    prompt: question,
    signal: controller.signal,
    onEvent(event) {
      if (event.type === 'done') {
        port.postMessage({ event: 'DONE' })
        return
      }
      port.postMessage(event.data)
    },
  })
}

Browser.runtime.onConnect.addListener((port) => {
  port.onMessage.addListener(async (msg) => {
    console.debug('received msg', msg)
    try {
      await generateAnswers(port, msg.question)
    } catch (err: any) {
      console.error(err)
      port.postMessage({ error: err.message })
    }
  })
})

Browser.runtime.onMessage.addListener(async (message) => {
  if (message.type === 'FEEDBACK') {
    const token = await getAI21AccessToken()
    await sendMessageFeedback(token, message.data)
  } else if (message.type === 'OPEN_OPTIONS_PAGE') {
    Browser.runtime.openOptionsPage()
  } else if (message.type === 'GET_ACCESS_TOKEN') {
    return getAI21AccessToken()
  }
})

Browser.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    Browser.runtime.openOptionsPage()
  }
})
