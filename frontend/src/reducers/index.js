import { FETCH_PARTICIPANTS_SUCCESS } from '../actions'

export default (state = {}, action) => {
  switch (action.type) {
    case FETCH_PARTICIPANTS_SUCCESS:
      console.log(action.payload)
      return action.payload
    default:
      return state
  }
}
