const NOTIFICATIONS = {
    'FAKE': {
        icon: '', color: '', title: ''
    },
    'MAYBE_FAKE': {
        icon: '', color: '', title: ''
    },
    'MAYBE_NOT_FAKE': {
        icon: '', color: '', title: ''
    },
    'NOT_FAKE': {
        icon: '', color: '', title: ''
    }
};

const ERRORS = {
    '400': { 
        icon: 'robot',
        color: '#222f3e',
        title: 'You have missed someting...',
        description: 'You need to tell us what is the news that you want to check :)' 
    },
    '503': { 
        icon: 'cloud-sync',
        color: '#2e86de',
        title: 'We are almost there... Hold on!',
        description: 'We are not ready yet, but we will be in a few moments!' 
    },
    'NO_NETWORK': { 
        icon: 'disconnect',
        color: '#ee5253',
        title: 'Ops..',
        description: 'It seems that we are offline :(' 
    }
};

function verify(data) {
    const { status, score } = data;
    return {
        title: NOTIFICATIONS[status].title,
        description: `The probability to not be fake is ${ score * 100 }%`,
        icon: NOTIFICATIONS[status].icon,
        iconColor: NOTIFICATIONS[status].color
    };
}

function verifyError(status) {
    return {
        title: ERRORS[status].title,
        description: ERRORS[status].description,
        icon: ERRORS[status].icon,
        iconColor: ERRORS[status].color
    };
}

export default { verify, verifyError };