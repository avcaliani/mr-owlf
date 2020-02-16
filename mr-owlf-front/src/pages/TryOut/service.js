export default function verify(content) {
    console.log('Received values of form: ', content);
    return {
        title: 'Sucesso na Recomendação!',
        description: 'Bla bla bla',
        icon: 'check',
        iconColor: 'green'
    }
}
