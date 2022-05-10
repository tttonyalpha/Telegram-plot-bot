from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from lib.graphics import GraphicPlotter
from telegram import ReplyKeyboardMarkup
import locale
locale.setlocale(locale.LC_ALL, "")


update_keyboard = ReplyKeyboardMarkup([['Изменить названия осей'], ['Изменить цвет графика'], [
    'Изменить название графика'], ['Не хочу ничего изменять']])
start_keyboard = ReplyKeyboardMarkup([['Начать']])
plot_keyboard = ReplyKeyboardMarkup([['Построить график']])
# заведем функцию start(),help(),error(), text() для обработки команд /start;/help и ответа на др сообщения


def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"Привет, {first_name}! Я могу нарисовать график по заданным точкам", reply_markup=start_keyboard)
    return 8


def help(update, context):
    my_help = ReplyKeyboardMarkup([['Help']])
    context.chat_data['help'] = 'help'
    update.message.reply_text('***')


def error(update, context):
    update.message.reply_text('Возникла ошибка при отправке')


def choice(update, context):  # промежуточное состояние выбора
    get_message = update.message.text
    if get_message == 'Изменить цвет графика':
        return change_color(update, context)
    elif get_message == 'Изменить названия осей':
        return change_aix(update, context)
    elif get_message == 'Изменить название графика':
        return name(update, context)
    elif get_message == 'Аппроксимировать':
        return approximation(update, context)
    elif get_message == 'Расположить точки по возрастанию':
        return points(update, context)
    elif get_message == 'Не хочу ничего изменять':
        return ask(update, context)


def ask(update, context):
    what_next_keyboard = ReplyKeyboardMarkup(
        [['Построить еще график'], ['Завершить работу']])
    update.message.reply_text(
        "Что хотите сделать дальше?", reply_markup=what_next_keyboard)
    return 9


def choice_2(update, context):
    get_message = update.message.text
    if get_message == 'Построить еще график':
        return plot(update, context)
    elif get_message == 'Завершить работу':
        return stop(update, context)


def plot(update, context):
    update.message.reply_text('Введите массив с данными')
    return 1


def graphic(update, context):
    plotter = GraphicPlotter()
    get_message = update.message.text
    error_keyboard = ReplyKeyboardMarkup([['Не хочу ничего изменять']])
    try:
        img = plotter.plot_from_string(get_message)
    except:
        update.message.reply_text(
            'Пожалуйста, введите точки графика в формате: "x y", причем строк должно быть больше двух', reply_markup=error_keyboard)
        get_message = update.message.text
        if get_message == 'Не хочу ничего изменять':
            what_next_keyboard = ReplyKeyboardMarkup(
                [['Построить еще график'], ['Завершить работу']])
            update.message.reply_text(
                "Что хотите сделать дальше?", reply_markup=what_next_keyboard)
            return 9
        else:
            return 1
    context.chat_data['base'] = get_message
    context.chat_data['color'] = 'blue'
    context.chat_data['x_label'] = 'Ось x'
    context.chat_data['y_label'] = 'Ось y'
    context.chat_data['title'] = 'График'
    context.bot.send_photo(chat_id=update.message.chat.id, photo=img)
    update.message.reply_text(
        'Хотите что-нибудь изменить?', reply_markup=update_keyboard)
    return 8


def change_color(update, context):
    my_keyboard = ReplyKeyboardMarkup(
        [['blue'], ['red'], ['black'], ['green'], ['yellow'], ['pink']])
    update.message.reply_text(
        'На какой цвет вы бы хотели поменять?', reply_markup=my_keyboard)
    return 2


def change_color_2(update, context):
    plotter = GraphicPlotter()
    update_keyboard_error = ReplyKeyboardMarkup(
        [['blue'], ['red'], ['black'], ['green'], ['yellow'], ['pink']])
    context.chat_data['color'] = update.message.text
    try:
        img1 = plotter.all_changes(context.chat_data['base'], context.chat_data['color'],
                                   context.chat_data['x_label'], context.chat_data['y_label'],
                                   context.chat_data['title'])
        context.bot.send_photo(chat_id=update.message.chat.id, photo=img1)
        update.message.reply_text(
            'Хотите ещё что-нибудь изменить?', reply_markup=update_keyboard)
    except:
        update.message.reply_text(
            'Пожалуйста, введите корректный цвет', reply_markup=update_keyboard_error)
        return 2
    return 8


def change_aix(update, context):
    update.message.reply_text('Введите название оси x')
    return 5


def change_aix_1(update, context):
    context.chat_data['x_label'] = update.message.text
    update.message.reply_text('Введите название оси y')
    return 3


def change_aix_2(update, context):
    context.chat_data['y_label'] = update.message.text
    plotter = GraphicPlotter()
    img1 = plotter.all_changes(context.chat_data['base'], context.chat_data['color'],
                               context.chat_data['x_label'], context.chat_data['y_label'],
                               context.chat_data['title'])
    context.bot.send_photo(chat_id=update.message.chat.id, photo=img1)
    update.message.reply_text(
        'Хотите ещё что-нибудь изменить?', reply_markup=update_keyboard)
    return 8


def name(update, context):
    update.message.reply_text('Введите новое название графика')
    return 4


def name_2(update, context):
    plotter = GraphicPlotter()
    context.chat_data['title'] = update.message.text
    img1 = plotter.all_changes(context.chat_data['base'], context.chat_data['color'],
                               context.chat_data['x_label'], context.chat_data['y_label'],
                               context.chat_data['title'])
    context.bot.send_photo(chat_id=update.message.chat.id, photo=img1)
    update.message.reply_text(
        'Хотите ещё что-нибудь изменить?', reply_markup=update_keyboard)
    return 8


def approximation(update, context):
    update.message.reply_text('*аппроксиморованный график*')  # меняем код
    update.message.reply_text(
        'Хотите ещё что-нибудь изменить?', reply_markup=update_keyboard)
    return 8


def points(update, context):
    update.message.reply_text(
        '*график с точками по возрастанию*')  # меняем код
    update.message.reply_text(
        'Хотите ещё что-нибудь изменить?', reply_markup=update_keyboard)
    return 8


''' 
когда мы завершим все изменения и получим желаемый графи, нужно отправить боту /stop или фразу "Не хочу ничего изменять",
 чтобы закончить диалог. автоматически этого не произойдет
 '''


def stop(update, context):
    update.message.reply_text(
        'Всегда рад помочь! До встречи!', reply_markup=start_keyboard)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    # команда для начала диалога в нашем случае plot
    # она просит ввести данные
    # список точек входа здесь может быть несколько команд или слов
    entry_points=[CommandHandler('plot', plot), ],

    # словарь состояний внутри диалога

    states={

        1: [MessageHandler(Filters.text & ~Filters.command, graphic)],
        2: [MessageHandler(Filters.text & ~Filters.command, change_color_2)],
        3: [MessageHandler(Filters.text & ~Filters.command, change_aix_2)],
        4: [MessageHandler(Filters.text & ~Filters.command, name_2)],
        5: [MessageHandler(Filters.text & ~Filters.command, change_aix_1)],
        8: [MessageHandler(Filters.text & ~Filters.command, choice)],
        9: [MessageHandler(Filters.text & ~Filters.command, choice_2)],
    },
    # точка прирывания диалога
    fallbacks=[CommandHandler('stop', stop)],
)


def text(update, context):
    text_received = update.message.text
    if text_received == "plot":
        return plot(update, context)
    else:
        update.message.reply_text('Я вас не понимаю(')


def main():

    #TOKEN = "5229182338:AAH738ZDXBDIYZoW3ZxQgRBpEPP16RZgXvI"
    #TOKEN = "5282803287:AAF01KIz-XbicvEBe1-1Djy3dYQYqqB_kCg"
    TOKEN = "5282803287:AAG03SBN1_Q3uyChhw9G1lFzaUX6fcpwO6w"

    # создаем средство обновления - updeter, которое также автоматически создаст диспетчер для обработки сообщений
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # добавляем обработчики для команд

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex("^Начать$"), start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("plot", plot))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(MessageHandler(
        Filters.regex("^Не хочу ничего изменять$"), stop))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Начать'), start))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('blue'), change_color))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('red'), change_color))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('black'), change_color))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('green'), change_color))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('yellow'), change_color))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('pink'), change_color))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), graphic))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), graphic))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), graphic))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), graphic))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), change_color_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), change_color_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), change_color_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), change_color_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), change_aix_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), change_aix_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), change_aix_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), change_aix_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), name_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), name_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), name_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), name_2))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), approximation))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), approximation))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), approximation))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), approximation))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить названия осей'), points))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить цвет графика'), points))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Изменить название графика'), points))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Не хочу ничего изменять'), points))

    # запускаем цикл приема и обработки сообщений
    updater.start_polling()
    # ждем завершения приложения при нажатии клавишь Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
