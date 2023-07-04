import { fetchSSE } from '../fetch-sse'
import { GenerateAnswerParams, Provider } from '../types'

export class AI21Provider implements Provider {
  constructor(private token: string, private model: string) {
    this.token = token
    this.model = model
  }

  private buildPrompt(prompt: string): string {
    if (this.model.startsWith('text-chat-davinci')) {
      return `Respond conversationally.\n\nUser: ${prompt}\nJurassic-2:`
    }
    return prompt
  }

  async generateAnswer(params: GenerateAnswerParams) {
    let result = ''
	let URL = `https://api.ai21.com/studio/v1/j2-${this.model}/complete`

    await fetchSSE(URL, {
      method: 'POST',

      headers: {
        "Content-Type": 'application/json',
        "Authorization": `Bearer ${this.token}`,
      },

	  body: JSON.stringify({
        "prompt": text,
        "numResults": 1,
        "maxTokens": params.maxTokens || 16,
        "temperature": params.temperature || 0.7,
        "topKReturn": params.topKReturn || 0,
        "topP": params.topP || 1,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": false,
            "applyToPunctuations": false,
            "applyToStopwords": false,
            "applyToWhitespaces": false,
            "applyToEmojis": false
        },
        "frequencyPenalty": {
            "scale": 0,
            "applyToNumbers": false,
            "applyToPunctuations": false,
            "applyToStopwords": false,
            "applyToWhitespaces": false,
            "applyToEmojis": false
        },
        "presencePenalty": {
            "scale": 0,
            "applyToNumbers": false,
            "applyToPunctuations": false,
            "applyToStopwords": false,
            "applyToWhitespaces": false,
            "applyToEmojis": false
        },
        "stopSequences": []
      }),

      onMessage(message) {
        console.debug('sse message', message)
        if (message === '[DONE]') {
          params.onEvent({ type: 'done' })
          return
        }
        let data
        try {
          data = JSON.parse(message)
          const text = data.choices[0].text
          if (text === '' || text === '') {
            return
          }
          result += text
          params.onEvent({
            type: 'answer',
            data: {
              text: result,
              messageId: data.id,
              conversationId: data.id,
            },
          })
        } catch (err) {
          console.error(err)
          return
        }
      },
    })
    return {}
  }
}
