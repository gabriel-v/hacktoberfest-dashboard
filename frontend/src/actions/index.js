import axios from 'axios'

const ROOT_URL = 'http://104.248.26.219/api'

export const FETCH_PARTICIPANTS_REQUEST = 'fetch_participants_request'
export const FETCH_PARTICIPANTS_SUCCESS = 'fetch_participants_success'

export const fetchParticipants = () => dispatch => {
  dispatch({ type: FETCH_PARTICIPANTS_REQUEST })

  axios.get(`${ROOT_URL}/events/1`).then(response =>
    dispatch({
      type: FETCH_PARTICIPANTS_SUCCESS,
      payload: response.data
    })
  )
}
